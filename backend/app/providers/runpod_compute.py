import time
import httpx
from typing import Dict, Any, Optional
from app.providers.base import ComputeProvider, ComputeJobOutput
from app.core.config import settings
from app.core.logging import logger


class RunPodComputeProvider(ComputeProvider):
    """
    RunPod Serverless GPU Compute Provider Adapter.
    Strictly used for heavy remote compute workloads (video rendering, heavy media processing, local inference).
    DO NOT route standard image generation or basic LLM calls through this provider.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.api_key = (api_key or settings.RUNPOD_API_KEY or settings.COMPUTE_API_KEY or "").strip()
        self.endpoint_id = (endpoint_id or settings.RUNPOD_ENDPOINT_ID or settings.COMPUTE_ENDPOINT_ID or "").strip()
        self.base_url = (base_url or "https://api.runpod.ai/v2").rstrip("/")

    @property
    def provider_name(self) -> str:
        return f"RunPodComputeProvider({self.endpoint_id or 'Unconfigured'})"

    def submit_job(
        self,
        task_type: str,
        payload: Dict[str, Any],
        timeout_s: int = 300
    ) -> ComputeJobOutput:
        start_time = time.time()

        if not self.api_key or not self.endpoint_id:
            logger.warning(f"{self.provider_name}: API Key or Endpoint ID missing. Returning simulated job.")
            return ComputeJobOutput(
                job_id="runpod_simulated_01",
                status="COMPLETED",
                result={"simulated": True, "message": "RunPod not configured; simulated heavy compute executed."},
                execution_time_ms=120
            )

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            body = {
                "input": {
                    "task_type": task_type,
                    **payload
                }
            }

            url = f"{self.base_url}/{self.endpoint_id}/run"
            with httpx.Client(timeout=15.0) as client:
                response = client.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()

            job_id = data.get("id", "unknown_job")
            status = data.get("status", "IN_QUEUE")

            # If sync run / completed immediately
            exec_time_ms = int((time.time() - start_time) * 1000)
            return ComputeJobOutput(
                job_id=job_id,
                status="COMPLETED" if status == "COMPLETED" else "RUNNING",
                result=data.get("output"),
                execution_time_ms=exec_time_ms
            )

        except Exception as e:
            logger.error(f"{self.provider_name} submit failed: {str(e)}")
            return ComputeJobOutput(
                job_id="failed_job",
                status="FAILED",
                error_message=str(e)
            )

    def get_job_status(self, job_id: str) -> ComputeJobOutput:
        if not self.api_key or not self.endpoint_id:
            return ComputeJobOutput(
                job_id=job_id,
                status="COMPLETED",
                result={"simulated": True}
            )

        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.base_url}/{self.endpoint_id}/status/{job_id}"
            with httpx.Client(timeout=15.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

            return ComputeJobOutput(
                job_id=job_id,
                status=data.get("status", "UNKNOWN"),
                result=data.get("output"),
                error_message=data.get("error")
            )
        except Exception as e:
            return ComputeJobOutput(
                job_id=job_id,
                status="FAILED",
                error_message=str(e)
            )

    def cancel_job(self, job_id: str) -> bool:
        if not self.api_key or not self.endpoint_id:
            return True
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.base_url}/{self.endpoint_id}/cancel/{job_id}"
            with httpx.Client(timeout=15.0) as client:
                response = client.post(url, headers=headers)
                return response.status_code in [200, 204]
        except Exception:
            return False
