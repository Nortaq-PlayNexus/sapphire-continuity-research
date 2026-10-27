"""CE-2 Experiment Runner."""
import json
import os
import sys
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path("C:/Users/natha/projects/ce-1-continuous-existence")))

from adapters.base import AdapterRegistry
from adapters.episodic_store import EpisodicStoreAdapter
from adapters.transcript import TranscriptAdapter
from adapters.app_state import AppStateAdapter


class CE2Runner:
    """Runner for CE-2 experiments."""
    
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = f"C:/tmp/ce2_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.registry = AdapterRegistry()
        self._register_adapters()
        self.run_id = f"ce2-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.results = []
    
    def _register_adapters(self):
        self.registry.register(EpisodicStoreAdapter())
        self.registry.register(TranscriptAdapter())
        self.registry.register(AppStateAdapter())
    
    def generate_scenarios(self, n_scenarios: int = 12, seed: int = 12345) -> List[Dict[str, Any]]:
        """Generate synthetic scenarios for testing."""
        rng = random.Random(seed)
        scenarios = []
        
        for i in range(n_scenarios):
            scenario_id = f"CE2_{i:03d}"
            # Generate unique facts
            code = f"CODE-{rng.randint(1000, 9999)}"
            value = rng.randint(100, 1000)
            entity = f"Entity{rng.randint(100, 999)}"
            
            fact = {
                "id": f"fact_{scenario_id}",
                "content": f"The secret {entity} uses access code {code} and has limit {value} requests.",
                "key": f"{entity}_code",
                "answer": code
            }
            
            episode = {
                "id": f"ep_{scenario_id}",
                "content": f"During session S-{i}, we discovered that {entity} uses access code {code} and has limit {value} requests per minute.",
                "context": f"Investigation of {entity}",
                "session_id": f"S-{i}",
                "event_type": "discovery",
                "tags": [entity.lower(), "discovery"]
            }
            
            transcript = [
                {"role": "user", "content": f"Investigate {entity}"},
                {"role": "assistant", "content": f"I'll look into {entity}. Let me start."},
                {"role": "user", "content": f"What access code does {entity} use and what is its limit?"},
                {"role": "assistant", "content": f"Based on our investigation, {entity} uses access code {code} and has limit {value} requests."}
            ]
            
            # Create decoy
            decoy_code = f"CODE-{rng.randint(1000, 9999)}"
            decoy_fact = {
                "id": f"decoy_{scenario_id}",
                "content": f"The secret {entity} uses access code {decoy_code} and has limit {value+50} requests.",
                "key": f"{entity}_code",
                "answer": decoy_code
            }
            decoy_episode = {
                "id": f"ep_decoy_{scenario_id}",
                "content": f"Earlier we thought {entity} uses access code {decoy_code} but that was from a different test.",
                "context": f"Test notes",
                "session_id": f"S-{i}-test",
                "event_type": "observation",
                "tags": [entity.lower(), "test"]
            }
            
            scenarios.append({
                "scenario_id": scenario_id,
                "entity": entity,
                "facts": [fact],
                "decoys": [decoy_fact],
                "episodes": [episode],
                "decoy_episodes": [decoy_episode],
                "transcript": transcript,
                "question": f"What access code does {entity} use?",
                "correct_answer": code,
                "decoy_answer": decoy_code,
                "session_id": f"S-{i}"
            })
        
        return scenarios
    
    def run_condition(self, condition_name: str, scenarios: List[Dict[str, Any]], 
                     adapters_to_use: List[str]) -> Dict[str, Any]:
        """Run a specific condition."""
        condition_results = {
            "condition": condition_name,
            "adapters": adapters_to_use,
            "scenarios": [],
            "start_time": datetime.now().isoformat()
        }
        
        for scenario in scenarios:
            scenario_result = {
                "scenario_id": scenario["scenario_id"],
                "question": scenario["question"],
                "correct_answer": scenario["correct_answer"],
                "retrieved": []
            }
            
            # Setup adapters for this scenario
            active_adapters = []
            for adapter_name in adapters_to_use:
                adapter = self.registry.get(adapter_name)
                if adapter and adapter_name == "episodic_store":
                    adapter.setup({"episodes": scenario["episodes"] + (scenario.get("decoy_episodes", []) if "decoy" in condition_name else [])})
                elif adapter and adapter_name == "transcript":
                    if "transcript" in condition_name or condition_name in ["C1", "C3"]:
                        adapter.setup(scenario)
                    else:
                        adapter.setup({"transcript": []})  # Empty
                elif adapter and adapter_name == "app_state":
                    adapter.setup(scenario)
                    if "restart" in condition_name or condition_name == "C4":
                        adapter.save_state()
                        # Simulate restart by creating new adapter instance state
                active_adapters.append(adapter)
            
            # Query
            query = scenario["question"]
            all_retrieved = []
            for adapter in active_adapters:
                if adapter and adapter.enabled:
                    try:
                        results = adapter.retrieve(query, {"n_results": 5})
                        all_retrieved.extend(results)
                    except Exception as e:
                        print(f"Error retrieving: {e}")
            
            scenario_result["retrieved"] = [
                {"content": r.content, "source_id": r.source_id, 
                 "confidence": r.confidence, "mechanism": r.mechanism}
                for r in all_retrieved
            ]
            
            # Check if correct answer found
            scenario_result["found_correct"] = any(
                scenario["correct_answer"] in r.content for r in all_retrieved
            )
            scenario_result["found_decoy"] = any(
                scenario.get("decoy_answer", "") in r.content for r in all_retrieved
            )
            
            condition_results["scenarios"].append(scenario_result)
            
            # Teardown
            for adapter in active_adapters:
                if adapter:
                    adapter.teardown()
        
        condition_results["end_time"] = datetime.now().isoformat()
        condition_results["n_scenarios"] = len(scenarios)
        condition_results["found_correct_rate"] = sum(1 for s in condition_results["scenarios"] if s["found_correct"]) / len(scenarios)
        condition_results["found_decoy_rate"] = sum(1 for s in condition_results["scenarios"] if s["found_decoy"]) / len(scenarios)
        
        return condition_results
    
    def run_all_conditions(self, n_scenarios: int = 12, seed: int = 12345) -> Dict[str, Any]:
        """Run all CE-2 conditions."""
        scenarios = self.generate_scenarios(n_scenarios, seed)
        
        conditions = [
            ("C0_fresh", []),
            ("C1_transcript", ["transcript"]),
            ("C2_episodic_real", ["episodic_store"]),
            ("C5_episodic_only_no_transcript", ["episodic_store"]),
            ("C6_transcript_only", ["transcript"]),
        ]
        
        all_results = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "n_scenarios": n_scenarios,
            "seed": seed,
            "conditions": []
        }
        
        for cond_name, adapters in conditions:
            print(f"Running condition {cond_name}...")
            result = self.run_condition(cond_name, scenarios, adapters)
            all_results["conditions"].append(result)
            print(f"  Found correct: {result['found_correct_rate']:.2%}, Found decoy: {result['found_decoy_rate']:.2%}")
        
        # Save results
        results_file = self.output_dir / f"{self.run_id}_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\nResults saved to {results_file}")
        return all_results


def main():
    runner = CE2Runner()
    results = runner.run_all_conditions(n_scenarios=12, seed=12345)
    return results


if __name__ == "__main__":
    main()
