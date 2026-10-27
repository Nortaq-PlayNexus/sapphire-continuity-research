"""Test application state recovery across process restart."""
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from adapters.app_state import AppStateAdapter


def test_save_state():
    """Test saving state."""
    adapter = AppStateAdapter(state_file="C:/tmp/test_restart_state.json")
    scenario = {
        "scenario_id": "TEST_001",
        "facts": [{"id": "f1", "content": "The code is TESTCODE123"}],
        "episodes": [{"id": "e1", "content": "We found TESTCODE123"}],
        "session_id": "S-1"
    }
    adapter.setup(scenario)
    result = adapter.save_state()
    assert result is True
    assert Path("C:/tmp/test_restart_state.json").exists()
    print("test_save_state PASSED")


def test_load_state():
    """Test loading state."""
    adapter = AppStateAdapter(state_file="C:/tmp/test_restart_state.json")
    result = adapter.load_from_disk()
    assert result is True
    assert adapter.app_state.get("scenario_id") == "TEST_001"
    results = adapter.retrieve("TESTCODE123", {"n_results": 5})
    assert len(results) > 0
    print("test_load_state PASSED")


def test_restart_simulation():
    """Simulate restart by creating new process."""
    # Write a script to run in separate process
    script = '''
import json
import sys
from pathlib import Path
sys.path.insert(0, r"C:/Users/natha/projects/sapphire-continuity-research")
from adapters.app_state import AppStateAdapter

adapter = AppStateAdapter(state_file="C:/tmp/test_restart_state.json")
result = adapter.load_from_disk()
if result:
    results = adapter.retrieve("TESTCODE123", {"n_results": 5})
    found = any("TESTCODE123" in r.content for r in results)
    print("FOUND:" + str(found))
    print("PID:" + str(__import__("os").getpid()))
    print("RESTORED:" + str(adapter.was_restored()))
else:
    print("FAILED")
'''
    script_path = Path("C:/tmp/test_restart_child.py")
    with open(script_path, 'w') as f:
        f.write(script)
    
    # Run in new process
    result = subprocess.run([sys.executable, str(script_path)], 
                          capture_output=True, text=True, timeout=10)
    print("Child output:", result.stdout)
    print("Child stderr:", result.stderr)
    
    assert "FOUND:True" in result.stdout
    assert "RESTORED:True" in result.stdout
    print("test_restart_simulation PASSED")
    
    # Cleanup
    Path("C:/tmp/test_restart_state.json").unlink(missing_ok=True)
    script_path.unlink(missing_ok=True)


if __name__ == "__main__":
    test_save_state()
    test_load_state()
    test_restart_simulation()
    print("\nAll restart tests passed!")
