import json
import base64
from pathlib import Path
import numpy as np
import cv2

def array_to_base64_jpeg(arr_bgr, quality=85):
    success, buffer = cv2.imencode('.jpg', arr_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not success:
        raise ValueError("Failed to encode image")
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

def depth_to_colormap(depth_meters, min_d=0.5, max_d=6.0, cmap=cv2.COLORMAP_TURBO):
    # Normalize depth to [0, 255]
    d_norm = np.clip((depth_meters - min_d) / (max_d - min_d), 0, 1)
    d_uint8 = (d_norm * 255).astype(np.uint8)
    # Apply colormap
    return cv2.applyColorMap(d_uint8, cmap)

def error_to_colormap(error_rel, max_err=0.35, cmap=cv2.COLORMAP_INFERNO):
    # Highlight high relative error
    e_norm = np.clip(error_rel / max_err, 0, 1)
    e_uint8 = (e_norm * 255).astype(np.uint8)
    return cv2.applyColorMap(e_uint8, cmap)

def main():
    results_path = Path("outputs/nyu_final/test/model_results.json")
    rgb_dir = Path("data/nyu/splits/test/rgb")
    depth_dir = Path("data/nyu/splits/test/depth")
    pred_dir = Path("outputs/alignment_ablation_full/test/predictions")
    out_json = Path("web_app/data/app_data.json")

    with open(results_path, "r", encoding="utf-8") as f:
        results_data = json.load(f)

    selected_scene_ids = ["scene_0049", "scene_0051", "scene_0052"]
    scenes_output = []

    records_by_id = {r["sample_id"]: r for r in results_data.get("records", [])}

    for sid in selected_scene_ids:
        if sid not in records_by_id:
            print(f"Warning: {sid} not found in model results")
            continue
        
        rec = records_by_id[sid]
        rgb_file = rgb_dir / f"{sid}.png"
        depth_file = depth_dir / f"{sid}.npy"
        pred_file = pred_dir / f"{sid}.npy"

        if not (rgb_file.exists() and depth_file.exists() and pred_file.exists()):
            print(f"Warning: files missing for {sid}")
            continue

        # Load RGB
        rgb_bgr = cv2.imread(str(rgb_file))
        rgb_rgb = cv2.cvtColor(rgb_bgr, cv2.COLOR_BGR2RGB)
        
        # Load Depth GT & Pred
        depth_gt = np.load(depth_file)
        pred_raw = np.load(pred_file)

        # Scale-shift alignment
        scale = rec["alignment"]["scale"]
        shift = rec["alignment"]["shift"]
        pred_aligned = 1.0 / np.maximum(scale * pred_raw + shift, 1e-6)

        # Relative error map
        valid_mask = np.isfinite(depth_gt) & (depth_gt > 0)
        error_rel = np.zeros_like(depth_gt)
        error_rel[valid_mask] = np.abs(pred_aligned[valid_mask] - depth_gt[valid_mask]) / depth_gt[valid_mask]

        # Colormaps
        depth_gt_bgr = depth_to_colormap(depth_gt, min_d=0.7, max_d=4.5)
        depth_pred_bgr = depth_to_colormap(pred_aligned, min_d=0.7, max_d=4.5)
        error_bgr = error_to_colormap(error_rel, max_err=0.30)

        # Base64 encodings
        rgb_b64 = array_to_base64_jpeg(rgb_bgr, quality=85)
        depth_gt_b64 = array_to_base64_jpeg(depth_gt_bgr, quality=85)
        depth_pred_b64 = array_to_base64_jpeg(depth_pred_bgr, quality=85)
        error_b64 = array_to_base64_jpeg(error_bgr, quality=85)

        # Process regions with ranking
        regions_list = []
        for reg in rec.get("regions", []):
            regions_list.append({
                "region_id": reg["region_id"],
                "bbox": reg["bbox"], # [x, y, w, h]
                "area": reg["area"],
                "mean_error": float(reg["mean_error"]),
                "features": {k: float(v) for k, v in reg["features"].items()},
                "scores": {k: float(v) for k, v in reg["scores"].items()},
                "top_cause": reg["top_cause"],
                "confidence": reg["confidence"],
                "score_margin": float(reg["score_margin"])
            })

        # Scene entry
        scene_entry = {
            "sample_id": sid,
            "title": f"NYU Test Split: {sid.upper()}",
            "description": "Dense real indoor scene captured via Microsoft Kinect RGB-D sensor.",
            "metrics": {
                "rmse": float(rec["metrics"]["rmse"]),
                "abs_rel": float(rec["metrics"]["abs_rel"]),
                "delta1": float(rec["metrics"]["delta1"]),
                "spearman": float(rec["metrics"]["spearman"]),
                "threshold": float(rec["threshold"]),
                "total_regions": len(regions_list)
            },
            "alignment": {
                "scale": float(scale),
                "shift": float(shift),
                "space": "inverse_depth"
            },
            "images": {
                "rgb": rgb_b64,
                "depth_gt": depth_gt_b64,
                "depth_pred": depth_pred_b64,
                "error_map": error_b64
            },
            "regions": regions_list
        }
        scenes_output.append(scene_entry)
        print(f"Processed {sid}: {len(regions_list)} failure regions.")

    # Write output JSON
    payload = {
        "version": "1.0",
        "models": ["Depth Anything V2 Small (ViT-Small)", "DPT-Hybrid-MiDaS (ResNet-50 + ViT)"],
        "dataset": "NYU Depth V2 Test Split (244 Scenes, Scene-Disjoint)",
        "scenes": scenes_output,
        "taxonomy": [
            {"id": "textureless", "label": "Textureless Surface", "desc": "Featureless planar walls, doors, ceilings with low gradient variance (variance < 200)."},
            {"id": "boundary_mixing", "label": "Boundary Mixing / Bleed", "desc": "Depth bleeding across high-frequency foreground/background object contours."},
            {"id": "reflection", "label": "Specular Reflection", "desc": "Non-Lambertian glares, mirrors, or glossy floor reflections with high HSV value and low saturation."},
            {"id": "thin_object", "label": "Thin Slender Structure", "desc": "Elongated geometries (chair legs, cords, poles) with bounding-box aspect ratio > 3.0."},
            {"id": "poor_lighting", "label": "Poor / Extreme Lighting", "desc": "Extreme underexposed shadow regions (brightness < 60) or overexposed glares (> 200)."},
            {"id": "occlusion", "label": "Occlusion Boundary", "desc": "Sharp depth step discontinuities across occluding foreground edges."},
            {"id": "ambiguous", "label": "Ambiguous / Multi-Cause", "desc": "Weak overall signal (score < 0.40) or competing hypotheses (score margin Delta < 0.10)."}
        ]
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\n[OK] Successfully generated web application data file at:")
    print(f"     {out_json.resolve()} (Size: {out_json.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()

