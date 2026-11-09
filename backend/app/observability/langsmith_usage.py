"""LangSmith-friendly LLM usage extraction and cost estimation for CTMS.

Actual provider usage is preferred. Costs are estimates unless OpenRouter/provider
billing metadata is available. Configure per-million-token rates in environment.
"""
import logging
import os
from typing import Any


from app.config.settings import settings
logger = settings.get_logger()

def _number(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def extract_usage(response: Any) -> dict:
    """Extract token usage from LangChain AIMessage and provider metadata."""
    usage = getattr(response, "usage_metadata", None) or {}
    response_metadata = getattr(response, "response_metadata", None) or {}
    provider_usage = response_metadata.get("token_usage") or response_metadata.get("usage") or {}

    input_tokens = _number(
        usage.get("input_tokens", provider_usage.get("prompt_tokens",
        provider_usage.get("input_tokens", 0)))
    )
    output_tokens = _number(
        usage.get("output_tokens", provider_usage.get("completion_tokens",
        provider_usage.get("output_tokens", 0)))
    )
    total_tokens = _number(
        usage.get("total_tokens", provider_usage.get("total_tokens", input_tokens + output_tokens))
    )
    if not total_tokens:
        total_tokens = input_tokens + output_tokens

    model_name = (
        response_metadata.get("model_name")
        or response_metadata.get("model")
        or os.getenv("model", "unknown")
    )

    # Rates are USD per 1 million tokens. Set these for the exact OpenRouter model.
    input_rate = _float_env("LLM_INPUT_COST_PER_1M_TOKENS")
    output_rate = _float_env("LLM_OUTPUT_COST_PER_1M_TOKENS")
    input_cost = input_tokens * input_rate / 1_000_000 if input_rate is not None else None
    output_cost = output_tokens * output_rate / 1_000_000 if output_rate is not None else None

    return {
        "model": str(model_name),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_cost_usd": round(input_cost, 10) if input_cost is not None else None,
        "output_cost_usd": round(output_cost, 10) if output_cost is not None else None,
        "total_cost_usd": round(input_cost + output_cost, 10)
            if input_cost is not None and output_cost is not None else None,
        "usage_source": "provider_usage" if (input_tokens or output_tokens) else "usage_unavailable",
        "cost_source": "configured_rate_estimate"
            if input_cost is not None and output_cost is not None else "rate_not_configured",
    }


def _float_env(name: str):
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        logger.warning("Invalid numeric configuration for %s", name)
        return None


def invoke_llm_with_usage(llm, messages, *, agent_name: str):
    """Invoke ChatOpenAI with LangSmith tags, then return response and usage."""
    config = {
        "tags": ["enterprise_ctms_copilot", f"agent:{agent_name}"],
        "metadata": {
            "application": "Enterprise_CTMS_Copilot",
            "agent_name": agent_name,
            "provider": "openrouter",
        },
    }
    response = llm.invoke(messages, config=config)
    usage = extract_usage(response)

    # Add custom usage/cost fields to the active LangSmith run when tracing is enabled.
    try:
        from langsmith.run_helpers import update_current_run
        update_current_run(metadata={
            "llm_model": usage["model"],
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
            "total_tokens": usage["total_tokens"],
            "input_cost_usd": usage["input_cost_usd"],
            "output_cost_usd": usage["output_cost_usd"],
            "total_cost_usd": usage["total_cost_usd"],
            "usage_source": usage["usage_source"],
            "cost_source": usage["cost_source"],
        })
    except Exception:
        # Tracing may be disabled or there may be no active parent run.
        pass

    return response, usage
