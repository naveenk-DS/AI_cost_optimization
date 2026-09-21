import pytest
from src.ai_cost_optimizer.services.cost_tracker import CostTracker

def test_normal_token_usage():
    tracker = CostTracker()
    result = tracker.calculate_cost("gpt-4o", 1000, 500)
    assert result["input_tokens"] == 1000
    assert result["output_tokens"] == 500
    assert result["estimated_cost"] == 0.0125

def test_zero_token_usage():
    tracker = CostTracker()
    result = tracker.calculate_cost("gpt-4o", 0, 0)
    assert result["estimated_cost"] == 0.0

def test_large_token_usage():
    tracker = CostTracker()
    # 1 million input, 2 million output
    result = tracker.calculate_cost("gpt-4o", 1000000, 2000000)
    # (1M * 5) + (2M * 15) = 5 + 30 = 35
    assert result["estimated_cost"] == 35.0

def test_different_model_pricing():
    tracker = CostTracker()
    # Test fallback pricing for unknown models (defaults to 0.20 per 1M)
    result = tracker.calculate_cost("unknown-provider", 1000000, 0)
    assert result["estimated_cost"] == 0.20

def test_invalid_negative_token_values():
    tracker = CostTracker()
    # It must raise a ValueError if we pass impossible physics (negative tokens)
    with pytest.raises(ValueError, match="Token counts cannot be negative"):
        tracker.calculate_cost("gpt-4o", -10, 500)

def test_local_model_handling():
    tracker = CostTracker()
    # Native local config tests
    # Using Llama 3.2 which falls back to local infra cost (0.20 in/0.20 out)
    result = tracker.calculate_cost("llama3.2", 2000000, 1000000)
    # (2M * 0.20) + (1M * 0.20) = 0.40 + 0.20 = 0.60
    assert result["estimated_cost"] == 0.60
