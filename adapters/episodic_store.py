"""Adapter for the real episodic-memory store."""
import sys
from pathlib import Path
from typing import Any, Dict, List
import json

# Add episodic-memory to path
sys.path.insert(0, str(Path("C:/Users/natha/projects/episodic-memory")))
# Try to use episodic-memory venv's site-packages if needed
venv_site = Path("C:/Users/natha/projects/episodic-memory/.venv/Lib/site-packages")
if venv_site.exists():
    sys.path.insert(0, str(venv_site))

try:
    from src.episodic_memory import EpisodicMemory, Episode
    EPISODIC_AVAILABLE = True
except Exception as e:
    EPISODIC_AVAILABLE = False
    print(f"Episodic memory not available: {e}")

from .base import PersistenceAdapter, RetrievalResult


class EpisodicStoreAdapter(PersistenceAdapter):
    """Use the actual episodic-memory ChromaDB store."""
    
    def __init__(self, persist_dir: str = None):
        super().__init__("episodic_store")
        if persist_dir is None:
            persist_dir = f"C:/tmp/ce2_episodic_{id(self)}"
        self.persist_dir = Path(persist_dir)
        self.memory = None
        self.stored_episodes = []
    
    def setup(self, scenario_data: Dict[str, Any]) -> bool:
        if not EPISODIC_AVAILABLE:
            return False
        
        try:
            self.memory = EpisodicMemory(persist_dir=str(self.persist_dir))
            # Store relevant episodes from scenario
            if "episodes" in scenario_data:
                for ep_data in scenario_data["episodes"]:
                    ep = Episode(
                        id=ep_data.get("id", ""),
                        content=ep_data.get("content", ""),
                        context=ep_data.get("context", ""),
                        session_id=ep_data.get("session_id", "ce2"),
                        event_type=ep_data.get("event_type", "observation"),
                        decisions=ep_data.get("decisions", []),
                        lessons=ep_data.get("lessons", []),
                        tags=ep_data.get("tags", []),
                    )
                    self.memory.remember(ep)
                    self.stored_episodes.append(ep.id)
            return True
        except Exception as e:
            print(f"Error setting up episodic store: {e}")
            return False
    
    def retrieve(self, query: str, context: Dict[str, Any]) -> List[RetrievalResult]:
        if not self.memory:
            return []
        
        try:
            results = self.memory.recall(query, n_results=context.get("n_results", 5))
            retrieval_results = []
            for r in results:
                retrieval_results.append(RetrievalResult(
                    content=r.get("document", ""),
                    source_id=r.get("id", ""),
                    confidence=r.get("similarity", 0.0),
                    metadata=r.get("metadata", {}),
                    mechanism="episodic_store"
                ))
            return retrieval_results
        except Exception as e:
            print(f"Error retrieving from episodic store: {e}")
            return []
    
    def teardown(self) -> bool:
        try:
            # Optionally clean up
            import shutil
            if self.persist_dir.exists():
                shutil.rmtree(self.persist_dir)
            return True
        except:
            return False
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "persist_dir": str(self.persist_dir),
            "stored_episodes": self.stored_episodes,
            "mechanism": "episodic_store"
        }
    
    def load_state(self, state: Dict[str, Any]) -> bool:
        try:
            self.persist_dir = Path(state["persist_dir"])
            self.stored_episodes = state.get("stored_episodes", [])
            if EPISODIC_AVAILABLE and self.persist_dir.exists():
                self.memory = EpisodicMemory(persist_dir=str(self.persist_dir))
                return True
        except Exception as e:
            print(f"Error loading episodic store state: {e}")
        return False
