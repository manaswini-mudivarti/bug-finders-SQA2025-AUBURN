#!/usr/bin/env bash
set -euo pipefail

# 1. Create & activate venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install all deps
pip install --upgrade pip
pip install -r requirements.txt

# 3. Static analysis
echo "🔍 Running Bandit…"
bandit -r . -f csv -o bandit_report.csv || true
if [[ -s bandit_report.csv ]]; then
  echo "❌ Bandit found issues:"
  cat bandit_report.csv
  # don't exit here if you want to still run fuzzing
fi

# 4. Graph analysis → fuzz targets
echo "🕸️  Building call‐graph & picking top‐5 functions…"
python graph_analysis.py

# 5. Dynamic fuzzing
echo "🧪 Running fuzzer…"
python fuzz.py

# 6. Summarize
echo
echo "✅ Simulation complete."
echo "  • Bandit report: $( [[ -f bandit_report.csv ]] && echo OK || echo MISSING )"
echo "  • Fuzz report:  $( [[ -f fuzz.csv ]] && echo OK || echo MISSING )"
