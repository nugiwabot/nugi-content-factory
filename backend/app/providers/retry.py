import time
from typing import Any, Callable, TypeVar

from app.core.errors import ProviderError
from app.core.logging import logger

T = TypeVar("T")


def call_with_retry(
    fn: Callable[..., T],
    *args: Any,
    attempts: int = 2,
    delay_seconds: float = 1.5,
    **kwargs: Any
) -> T:
    """
    Calls a provider function and retries transient failures a bounded number of
    times. Configuration errors ("not configured") are never retried and always
    propagate immediately. After exhausting attempts the last ProviderError is
    re-raised so the caller sees a real failure (never a silent mock success).
    """
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn(*args, **kwargs)
        except ProviderError as e:
            if "not configured" in e.message.lower():
                raise
            last_error = e
            if attempt < attempts:
                logger.warning(
                    f"Provider call failed (attempt {attempt}/{attempts}): {e.message}. Retrying in {delay_seconds}s."
                )
                time.sleep(delay_seconds)
    assert last_error is not None
    raise last_error
