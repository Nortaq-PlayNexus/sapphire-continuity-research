import os, json, subprocess
from pathlib import Path
from datetime import datetime

base = Path('C:/Users/natha/projects/sapphire-continuity-research')
baseline = {'timestamp': datetime.now().isoformat(), 'repos_audited': []}
repos = ['C:/Users/natha/projects/ce-1-continuous-existence', 'C:/Users/natha/projects/episodic-memory', 'C:/Users/natha/ScientificDiscoveryLab']
for r in repos:
    if os.path.exists(r):
        try:
            res = subprocess.run(['git', '-C', r, 'log', '--oneline', '-1'], capture_output=True, text=True)
            branch = subprocess.run(['git', '-C', r, 'branch', '--show-current'], capture_output=True, text=True)
            status = subprocess.run(['git', '-C', r, 'status', '--short'], capture_output=True, text=True)
            baseline['repos_audited'].append({'path': r, 'commit': res.stdout.strip(), 'branch': branch.stdout.strip(), 'dirty': len(status.stdout.strip())>0})
        except Exception as e:
            baseline['repos_audited'].append({'path': r, 'error': str(e)})
    else:
        baseline['repos_audited'].append({'path': r, 'exists': False})
with open(base / 'AUDIT_BASELINE.json','w') as f:
    json.dump(baseline,f,indent=2)
print(json.dumps(baseline, indent=2))
