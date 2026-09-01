import time
from typing import Dict, Any, Optional
from app.providers.base import ComputeProvider, ComputeJobOutput


class MockComputeProvider(ComputeProvider):
    """
    Deterministic Mock Compute Provider for fast offline testing.
    """
    def __init__(self):
        self._jobs: Dict[str, ComputeJobOutput] = {}

    @property
    def provider_name(self) -> str:
        return "MockComputeProvider"

    def submit_job(
        self,
        task_type: str,
        payload: Dict[str, Any],
        timeout_s: int = 300
    ) -> ComputeJobOutput:
        job_id = f"mock_job_{len(self._jobs) + 1}"
        output = ComputeJobOutput(
            job_id=job_id,
            status="COMPLETED",
            result={"task_type": task_type, "status": "mock_success", "payload": payload},
            output_files=["mock_output.mp4"],
            execution_time_ms=10
        )
        self._jobs[job_id] = output
        return output

    def get_job_status(self, job_id: str) -> ComputeJobOutput:
        return self._jobs.get(
            job_id,
            ComputeJobOutput(job_id=job_id, status="COMPLETED", result={"mock": True})
        )

    def cancel_job(self, job_id: str) -> bool:
        if job_id in self._jobs:
            self._jobs[job_id].status = "CANCELLED"
            return True
        return True
