import time
import uuid
from typing import Dict, Any, Optional
from app.providers.base import ComputeProvider, ComputeJobOutput
from app.core.logging import logger


class LocalComputeProvider(ComputeProvider):
    """
    Local in-process Compute Provider.
    Executes tasks on the host machine without external GPU/cloud dependencies.
    """
    def __init__(self):
        self._jobs: Dict[str, ComputeJobOutput] = {}

    @property
    def provider_name(self) -> str:
        return "LocalComputeProvider(In-Process)"

    def submit_job(
        self,
        task_type: str,
        payload: Dict[str, Any],
        timeout_s: int = 300
    ) -> ComputeJobOutput:
        start_time = time.time()
        job_id = f"local_job_{uuid.uuid4().hex[:10]}"

        logger.info(f"LocalComputeProvider: Executing task '{task_type}' (job {job_id})")

        # Execute simulated or local processing
        res = {
            "task_type": task_type,
            "processed_locally": True,
            "received_keys": list(payload.keys())
        }

        exec_time_ms = int((time.time() - start_time) * 1000)
        output = ComputeJobOutput(
            job_id=job_id,
            status="COMPLETED",
            result=res,
            output_files=[],
            execution_time_ms=exec_time_ms
        )
        self._jobs[job_id] = output
        return output

    def get_job_status(self, job_id: str) -> ComputeJobOutput:
        if job_id in self._jobs:
            return self._jobs[job_id]
        return ComputeJobOutput(
            job_id=job_id,
            status="FAILED",
            error_message=f"Job '{job_id}' not found in local job registry."
        )

    def cancel_job(self, job_id: str) -> bool:
        if job_id in self._jobs:
            self._jobs[job_id].status = "CANCELLED"
            return True
        return False
