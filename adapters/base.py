"""Base adapter interface for persistence mechanisms."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json
from pathlib import Path


@dataclass
class RetrievalResult:
    """Result from a persistence mechanism."""
    content: str
    source_id: str
    confidence: float
    metadata: Dict[str, Any]
    mechanism: str  # which mechanism provided it


class PersistenceAdapter(ABC):
    """Base class for all persistence mechanisms."""
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
    
    @abstractmethod
    def setup(self, scenario_data: Dict[str, Any]) -> bool:
        """Setup the adapter with scenario data."""
        pass
    
    @abstractmethod
    def retrieve(self, query: str, context: Dict[str, Any]) -> List[RetrievalResult]:
        """Retrieve relevant information."""
        pass
    
    @abstractmethod
    def teardown(self) -> bool:
        """Clean up after experiment."""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Get current state for saving."""
        pass
    
    @abstractmethod
    def load_state(self, state: Dict[str, Any]) -> bool:
        """Load state from saved state."""
        pass


class AdapterRegistry:
    """Registry of available adapters."""
    
    def __init__(self):
        self.adapters: Dict[str, PersistenceAdapter] = {}
    
    def register(self, adapter: PersistenceAdapter):
        self.adapters[adapter.name] = adapter
    
    def get(self, name: str) -> Optional[PersistenceAdapter]:
        return self.adapters.get(name)
    
    def list(self) -> List[str]:
        return list(self.adapters.keys())
