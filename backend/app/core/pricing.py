"""
Lightweight cost estimation for AI provider usage.

Static price table (USD). Editable by hand. Values are estimates used to answer
"How much did this batch cost?" - not a billing system. Unknown models return
None ("unpriced") instead of crashing.
"""

from typing import Dict, Optional, Tuple


# LLM price table: model substring -> (USD per 1M input tokens, USD per 1M output tokens)
# Substrings are matched case-insensitively against "provider/model".
LLM_PRICES: Dict[str, Tuple[float, float]] = {
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "gemini-3.1-flash-lite": (0.30, 2.50),
    "gemini-2.5-flash-lite": (0.30, 2.50),
    "gemini-2.0-flash": (0.10, 0.40),
    "gemini-1.5-flash": (0.075, 0.30),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "claude-3-5-sonnet": (3.00, 15.00),
    "claude-3-haiku": (0.25, 1.25),
    "claude-sonnet-4": (3.00, 15.00),
    "claude-haiku": (0.80, 4.00),
    "deepseek": (0.27, 1.10),
}

# Image price table: model substring -> (USD per image)
IMAGE_PRICES: Dict[str, float] = {
    "flux-pro-1.1": 0.04,
    "flux-1.1-pro": 0.04,
    "flux-2-klein-9b": 0.04,
    "flux-1-dev": 0.03,
    "flux-dev": 0.025,
    "flux-1-schnell": 0.003,
    "flux-schnell": 0.003,
    "dall-e-3": 0.08,
    "dall-e-2": 0.02,
}

DEFAULT_LLM_INPUT_PER_1M = 0.30
DEFAULT_LLM_OUTPUT_PER_1M = 1.20
DEFAULT_IMAGE_PRICE = 0.05


def estimate_llm_cost(
    model: Optional[str],
    tokens_in: Optional[int],
    tokens_out: Optional[int],
) -> Optional[float]:
    """Estimates USD cost for an LLM call. Returns None when unpriced/unknown tokens."""
    if not model or tokens_in is None:
        return None
    out_tokens = tokens_out if tokens_out is not None else 0
    prices = _lookup_llm(model)
    if prices is None:
        return None
    in_rate, out_rate = prices
    return round((tokens_in / 1_000_000) * in_rate + (out_tokens / 1_000_000) * out_rate, 6)


def estimate_image_cost(model: Optional[str]) -> Optional[float]:
    """Estimates USD cost for a single image generation."""
    if not model:
        return None
    for key, price in IMAGE_PRICES.items():
        if key.lower() in model.lower():
            return price
    return None


def _lookup_llm(model: str) -> Optional[Tuple[float, float]]:
    lowered = model.lower()
    for key, prices in LLM_PRICES.items():
        if key.lower() in lowered:
            return prices
    return None
