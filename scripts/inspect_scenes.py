import json
from pathlib import Path

with open("outputs/nyu_final/test/model_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total test scenes: {len(data['records'])}")
for r in data["records"][:15]:
    causes = [reg["top_cause"] for reg in r.get("regions", [])]
    cause_summary = ", ".join(f"{c}: {causes.count(c)}" for c in sorted(set(causes)))
    print(f"{r['sample_id']} | RMSE: {r['metrics']['rmse']:.4f}m | AbsRel: {r['metrics']['abs_rel']:.4f} | Regions: {len(r['regions'])} | ({cause_summary})")

