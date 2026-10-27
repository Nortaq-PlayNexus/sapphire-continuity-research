"""Adapter for transcript replay."""
from typing import Any, Dict, List
from .base import PersistenceAdapter, RetrievalResult


class TranscriptAdapter(PersistenceAdapter):
    """Replay conversation transcript."""
    
    def __init__(self):
        super().__init__("transcript")
        self.transcript = []
    
    def setup(self, scenario_data: Dict[str, Any]) -> bool:
        try:
            if "transcript" in scenario_data:
                self.transcript = scenario_data["transcript"]
            elif "episodes" in scenario_data:
                # Build transcript from episodes
                for ep in scenario_data["episodes"]:
                    self.transcript.append({
                        "role": "system" if ep.get("role") == "system" else "user",
                        "content": ep.get("content", "")
                    })
            return True
        except Exception as e:
            print(f"Error setting up transcript: {e}")
            return False
    
    def retrieve(self, query: str, context: Dict[str, Any]) -> List[RetrievalResult]:
        # For transcript, we return relevant parts based on simple matching
        results = []
        for i, msg in enumerate(self.transcript):
            if any(word.lower() in msg.get("content", "").lower() 
                   for word in query.split() if len(word) > 3):
                results.append(RetrievalResult(
                    content=msg.get("content", ""),
                    source_id=f"transcript_{i}",
                    confidence=0.8,
                    metadata={"index": i, "role": msg.get("role")},
                    mechanism="transcript"
                ))
        # Return most relevant first (simple)
        return results[:context.get("n_results", 5)]
    
    def teardown(self) -> bool:
        self.transcript = []
        return True
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "mechanism": "transcript"
        }
    
    def load_state(self, state: Dict[str, Any]) -> bool:
        try:
            self.transcript = state.get("transcript", [])
            return True
        except:
            return False
    
    def get_full_transcript(self) -> str:
        """Get full transcript as formatted string."""
        lines = []
        for msg in self.transcript:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")
        return "\n\n".join(lines)
