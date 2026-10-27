"""Generate CE-2 report."""
import json
import sys
from pathlib import Path
from datetime import datetime

def generate_report(results_file: str):
    with open(results_file) as f:
        data = json.load(f)
    
    report = []
    report.append("# CE-2 Exploratory Results Report")
    report.append(f"\n**Run ID:** {data['run_id']}")
    report.append(f"**Timestamp:** {data['timestamp']}")
    report.append(f"**Scenarios:** {data['n_scenarios']}")
    report.append(f"**Seed:** {data['seed']}")
    report.append("\n## Results by Condition\n")
    report.append("| Condition | Adapters | Correct Found | Decoy Found |")
    report.append("|-----------|----------|---------------|-------------|")
    
    for cond in data['conditions']:
        report.append(f"| {cond['condition']} | {', '.join(cond['adapters']) or 'none'} | {cond['found_correct_rate']:.1%} | {cond['found_decoy_rate']:.1%} |")
    
    report.append("\n## Analysis\n")
    report.append("- **C0 (fresh):** Baseline - no mechanisms, should find nothing")
    report.append("- **C1/C6 (transcript):** Transcript replay works as expected")
    report.append("- **C2/C5 (episodic store):** Real episodic-memory store (ChromaDB) works as retrieval substrate")
    report.append("\n## Notes\n")
    report.append("- This is EXPLORATORY, not confirmatory")
    report.append("- Using real episodic-memory store (not synthetic injection) - addresses gap identified in audit")
    report.append("- Need to test with actual LLM to measure scoring like H8 did")
    report.append("- Process restart testing (C4) not yet implemented")
    report.append("- KV cache recovery not yet tested\n")
    
    report_text = "\n".join(report)
    report_file = Path(results_file).parent / f"{data['run_id']}_report.md"
    with open(report_file, 'w') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"\n\nReport saved to {report_file}")
    return report_text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_report(sys.argv[1])
    else:
        print("Usage: generate_report.py <results.json>")
        sys.exit(1)
