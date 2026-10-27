"""Adapter for application-level state reconstruction."""
import json
import os
import pickle
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
from .base import PersistenceAdapter, RetrievalResult


class AppStateAdapter(PersistenceAdapter):
    """Save and restore application state across process restart."""
    
    def __init__(self, state_file: str = None):
        super().__init__("app_state")
        if state_file is None:
            state_file = f"C:/tmp/ce2_appstate_{id(self)}.json"
        self.state_file = Path(state_file)
        self.app_state = {}
        self.process_id = os.getpid()
    
    def setup(self, scenario_data: Dict[str, Any]) -> bool:
        try:
            # Initialize app state from scenario
            self.app_state = {
                "scenario_id": scenario_data.get("scenario_id"),
                "facts": scenario_data.get("facts", []),
                "context": scenario_data.get("context", {}),
                "session_id": scenario_data.get("session_id"),
                "created_at": datetime.now().isoformat(),
                "process_id": self.process_id,
                "episodes": scenario_data.get("episodes", [])
            }
            return True
        except Exception as e:
            print(f"Error setting up app state: {e}")
            return False
    
    def save_state(self) -> bool:
        """Save state to disk (for restart testing)."""
        try:
            self.app_state["saved_at"] = datetime.now().isoformat()
            self.app_state["saved_by_pid"] = os.getpid()
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.app_state, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving app state: {e}")
            return False
    
    def load_from_disk(self) -> bool:
        """Load state from disk (simulating restart)."""
        try:
            if not self.state_file.exists():
                return False
            with open(self.state_file, 'r', encoding='utf-8') as f:
                self.app_state = json.load(f)
            self.app_state["loaded_at"] = datetime.now().isoformat()
            self.app_state["loaded_by_pid"] = os.getpid()
            return True
        except Exception as e:
            print(f"Error loading app state: {e}")
            return False
    
    def retrieve(self, query: str, context: Dict[str, Any]) -> List[RetrievalResult]:
        results = []
        # Search in saved state
        for fact in self.app_state.get("facts", []):
            fact_content = fact.get("content", str(fact))
            if any(word.lower() in fact_content.lower() 
                   for word in query.split() if len(word) > 3):
                results.append(RetrievalResult(
                    content=fact_content,
                    source_id=fact.get("id", "fact"),
                    confidence=0.9,
                    metadata=fact,
                    mechanism="app_state"
                ))
        
        for ep in self.app_state.get("episodes", []):
            ep_content = ep.get("content", "")
            if any(word.lower() in ep_content.lower() 
                   for word in query.split() if len(word) > 3):
                results.append(RetrievalResult(
                    content=ep_content,
                    source_id=ep.get("id", "ep"),
                    confidence=0.9,
                    metadata=ep,
                    mechanism="app_state"
                ))
        
        return results[:context.get("n_results", 5)]
    
    def teardown(self) -> bool:
        try:
            if self.state_file.exists():
                self.state_file.unlink()
        except:
            pass
        self.app_state = {}
        return True
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "state_file": str(self.state_file),
            "app_state": self.app_state,
            "mechanism": "app_state"
        }
    
    def load_state(self, state: Dict[str, Any]) -> bool:
        try:
            self.state_file = Path(state["state_file"])
            self.app_state = state.get("app_state", {})
            return True
        except:
            return False
    
    def was_restored(self) -> bool:
        """Check if state was loaded from a different process."""
        loaded_pid = self.app_state.get("loaded_by_pid")
        saved_pid = self.app_state.get("saved_by_pid")
        if loaded_pid and saved_pid and loaded_pid != saved_pid:
            return True
        return loaded_pid is not None and saved_pid is None
