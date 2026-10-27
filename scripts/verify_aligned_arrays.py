import numpy as np
from pathlib import Path
import json

test_scenes = ["scene_0049", "scene_0051", "scene_0052", "scene_0098"]
depth_dir = Path("data/nyu/splits/test/depth")
pred_dir = Path("outputs/alignment_ablation_full/test/predictions")

with open("outputs/nyu_final/test/model_results.json", "r") as f:
    results = json.load(f)
records = {r["sample_id"]: r for r in results["records"]}

for sid in test_scenes:
    gt = np.load(depth_dir / f"{sid}.npy")
    raw_pred = np.load(pred_dir / f"{sid}.npy")
    rec = records[sid]
    scale = rec["alignment"]["scale"]
    shift = rec["alignment"]["shift"]
    aligned_pred = 1.0 / np.maximum(scale * raw_pred + shift, 1e-6)
    
    print(f"{sid}: GT shape={gt.shape}, range=[{gt.min():.3f}, {gt.max():.3f}] m")
    print(f"       Pred shape={aligned_pred.shape}, range=[{aligned_pred.min():.3f}, {aligned_pred.max():.3f}] m")
    abs_err = np.abs(aligned_pred - gt)
    rel_err = abs_err / gt
    print(f"       Mean AbsErr={abs_err.mean():.4f} m, Mean RelErr={rel_err.mean():.4f}")

