"""Tests for CE-2 adapters."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.base import AdapterRegistry, RetrievalResult
from adapters.transcript import TranscriptAdapter


def test_transcript_adapter():
    adapter = TranscriptAdapter()
    scenario = {
        "transcript": [
            {"role": "user", "content": "What is the code?"},
            {"role": "assistant", "content": "The code is ABC123"}
        ]
    }
    assert adapter.setup(scenario) == True
    results = adapter.retrieve("code", {"n_results": 5})
    assert len(results) > 0
    assert any("ABC123" in r.content for r in results)
    assert adapter.teardown() == True
    print("test_transcript_adapter PASSED")


def test_adapter_registry():
    registry = AdapterRegistry()
    adapter = TranscriptAdapter()
    registry.register(adapter)
    assert registry.get("transcript") is not None
    assert "transcript" in registry.list()
    print("test_adapter_registry PASSED")


if __name__ == "__main__":
    test_transcript_adapter()
    test_adapter_registry()
    print("\nAll adapter tests passed!")
