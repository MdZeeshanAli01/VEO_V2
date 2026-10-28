import json
import base64
import sys
from pathlib import Path
import numpy as np
import cv2
import torch
from PIL import Image

sys.path.insert(0, str(Path("src").resolve()))
sys.path.insert(0, str(Path("official/Depth-Anything-V2").resolve()))
sys.path.insert(0, str(Path("official/Depth-Anything-V2/metric_depth").resolve()))

from depth_anything_v2.dpt import DepthAnythingV2

def array_to_base64_jpeg(arr_bgr, quality=88):
    success, buffer = cv2.imencode('.jpg', arr_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not success:
        raise ValueError("Failed to encode image")
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode('ascii')

def array_to_base64_png(arr_bgr):
    success, buffer = cv2.imencode('.png', arr_bgr)
    if not success:
        raise ValueError("Failed to encode image")
    return "data:image/png;base64," + base64.b64encode(buffer).decode('ascii')

def encode_depth_uint16_b64(depth_meters):
    # Quantize depth to millimeters [0, 65535]
    depth_mm = np.clip(np.round(depth_meters * 1000.0), 0, 65535).astype(np.uint16)
    return base64.b64encode(depth_mm.tobytes()).decode("ascii")

def depth_to_colormap(depth_meters, min_d=0.7, max_d=4.5, cmap=cv2.COLORMAP_TURBO):
    d_norm = np.clip((depth_meters - min_d) / (max_d - min_d), 0, 1)
    d_uint8 = (d_norm * 255).astype(np.uint8)
    return cv2.applyColorMap(d_uint8, cmap)

def error_to_colormap(error_rel, max_err=0.35, cmap=cv2.COLORMAP_INFERNO):
    e_norm = np.clip(error_rel / max_err, 0, 1)
    e_uint8 = (e_norm * 255).astype(np.uint8)
    return cv2.applyColorMap(e_uint8, cmap)

def main():
    print("Loading Depth Anything V2 model for authentic activation extraction...")
    checkpoint = Path("checkpoints/depth_anything_v2_metric_hypersim_vits.pth")
    configs = {"encoder": "vits", "features": 64, "out_channels": [48, 96, 192, 384], "max_depth": 20.0}
    model = DepthAnythingV2(**configs)
    model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
    model.eval()

    # Register forward hooks on intermediate transformer blocks [2, 5, 8, 11] (layers 3, 6, 9, 12)
    activations = {}
    def make_hook(name):
        def hook(m, inp, out):
            activations[name] = out
        return hook

    for idx in [2, 5, 8, 11]:
        model.pretrained.blocks[idx].register_forward_hook(make_hook(f"layer_{idx+1}"))

    # Load alignment records
    results_path = Path("outputs/nyu_final/test/model_results.json")
    with open(results_path, "r", encoding="utf-8") as f:
        results_data = json.load(f)
    records_by_id = {r["sample_id"]: r for r in results_data.get("records", [])}

    # Curate 4 diverse test scenes
    selected_scenes = [
        {
            "id": "scene_0049",
            "title": "Living Room: Planar Walls & Workstation",
            "category_focus": "Textureless Surface",
            "default_region": {"x": 210, "y": 140, "desc": "Large planar wall above workstation desk"}
        },
        {
            "id": "scene_0051",
            "title": "Office: Cluttered Chair & Bookshelf",
            "category_focus": "Boundary Mixing & Bleed",
            "default_region": {"x": 260, "y": 280, "desc": "High-frequency chair backrest and desk boundary"}
        },
        {
            "id": "scene_0052",
            "title": "Classroom / Lab: Fluorescent Light & Glossy Glare",
            "category_focus": "Specular Reflection & Lighting",
            "default_region": {"x": 420, "y": 120, "desc": "Fluorescent fixture specular reflection on whiteboard"}
        },
        {
            "id": "scene_0098",
            "title": "Corridor: Occluding Edges & Slender Geometries",
            "category_focus": "Occlusion & Thin Structures",
            "default_region": {"x": 310, "y": 220, "desc": "Sharp depth step edge of doorframe occluding back hallway"}
        }
    ]

    rgb_dir = Path("data/nyu/splits/test/rgb")
    depth_dir = Path("data/nyu/splits/test/depth")
    pred_dir = Path("outputs/alignment_ablation_full/test/predictions")
    out_js = Path("web_app/data/app_data_v2.js")

    scenes_output = []

    for item in selected_scenes:
        sid = item["id"]
        print(f"\nProcessing {sid} ({item['title']})...")
        rec = records_by_id.get(sid)
        if not rec:
            print(f"Skipping {sid}, no record found")
            continue

        rgb_file = rgb_dir / f"{sid}.png"
        depth_file = depth_dir / f"{sid}.npy"
        pred_file = pred_dir / f"{sid}.npy"

        # Load RGB
        rgb_bgr = cv2.imread(str(rgb_file))
        rgb_rgb = cv2.cvtColor(rgb_bgr, cv2.COLOR_BGR2RGB)
        h, w = rgb_bgr.shape[:2]

        # Load GT Depth
        depth_gt = np.load(depth_file).astype(np.float32)

        # Scale-shift alignment
        scale = rec["alignment"]["scale"]
        shift = rec["alignment"]["shift"]
        raw_pred = np.load(pred_file).astype(np.float32)
        pred_aligned = 1.0 / np.maximum(scale * raw_pred + shift, 1e-6)

        # Compute error maps
        valid_mask = np.isfinite(depth_gt) & (depth_gt > 0)
        abs_err = np.zeros_like(depth_gt)
        rel_err = np.zeros_like(depth_gt)
        abs_err[valid_mask] = np.abs(pred_aligned[valid_mask] - depth_gt[valid_mask])
        rel_err[valid_mask] = abs_err[valid_mask] / depth_gt[valid_mask]

        # Extract authentic intermediate model activations
        activations.clear()
        with torch.no_grad():
            img_tensor, (orig_h, orig_w) = model.image2tensor(rgb_bgr, input_size=518)
            patch_h, patch_w = img_tensor.shape[-2] // 14, img_tensor.shape[-1] // 14
            _ = model.forward(img_tensor)

        feature_maps = {}
        layer_desc = {
            "layer_3": "Layer 3 (Early Stage): Low-level gradient filters, edge tokens, and local contrast transitions.",
            "layer_6": "Layer 6 (Mid Stage): Textural grouping, local surface geometry, and orientation patches.",
            "layer_9": "Layer 9 (Semantic Stage): Object part boundaries and relational spatial clustering.",
            "layer_12": "Layer 12 (Global Stage): Scene-level semantic layout, planar priors, and horizon context."
        }

        for layer_name in ["layer_3", "layer_6", "layer_9", "layer_12"]:
            token_feat = activations[layer_name][:, 1:, :] # [1, N, 384]
            # Activation magnitude (L2 norm along channel dimension)
            mag = torch.norm(token_feat[0], dim=-1).reshape(patch_h, patch_w).numpy()
            mag_norm = (mag - mag.min()) / (mag.max() - mag.min() + 1e-6)
            mag_uint8 = (mag_norm * 255).astype(np.uint8)
            mag_color = cv2.applyColorMap(mag_uint8, cv2.COLORMAP_VIRIDIS)
            mag_resized = cv2.resize(mag_color, (w, h), interpolation=cv2.INTER_CUBIC)
            feature_maps[layer_name] = {
                "image": array_to_base64_jpeg(mag_resized, quality=85),
                "description": layer_desc[layer_name],
                "tokens_shape": [patch_h, patch_w, 384],
                "min_act": float(mag.min()),
                "max_act": float(mag.max())
            }

        # Colormapped visuals
        min_depth_vis = float(np.percentile(depth_gt[valid_mask], 1.0))
        max_depth_vis = float(np.percentile(depth_gt[valid_mask], 99.0))
        depth_gt_bgr = depth_to_colormap(depth_gt, min_d=min_depth_vis, max_d=max_depth_vis)
        depth_pred_bgr = depth_to_colormap(pred_aligned, min_d=min_depth_vis, max_d=max_depth_vis)
        error_bgr = error_to_colormap(rel_err, max_err=0.35)

        # Full 16-bit millimeter depth encodings
        gt_b64_uint16 = encode_depth_uint16_b64(depth_gt)
        pred_b64_uint16 = encode_depth_uint16_b64(pred_aligned)

        # Downsampled 3D point cloud grid (60x80)
        sub_y = np.linspace(0, h - 1, 60, dtype=int)
        sub_x = np.linspace(0, w - 1, 80, dtype=int)
        mesh_gt = depth_gt[np.ix_(sub_y, sub_x)].round(3).tolist()
        mesh_pred = pred_aligned[np.ix_(sub_y, sub_x)].round(3).tolist()
        mesh_rgb = (rgb_rgb[np.ix_(sub_y, sub_x)] / 255.0).round(2).tolist()

        # Precomputed failure regions
        regions_list = []
        for reg in rec.get("regions", []):
            regions_list.append({
                "region_id": reg["region_id"],
                "bbox": reg["bbox"],
                "area": reg["area"],
                "mean_error": float(reg["mean_error"]),
                "features": {k: float(v) for k, v in reg["features"].items()},
                "scores": {k: float(v) for k, v in reg["scores"].items()},
                "top_cause": reg["top_cause"],
                "confidence": reg["confidence"],
                "score_margin": float(reg["score_margin"])
            })

        scene_entry = {
            "sample_id": sid,
            "title": item["title"],
            "category_focus": item["category_focus"],
            "default_region": item["default_region"],
            "width": w,
            "height": h,
            "depth_range": [round(float(depth_gt[valid_mask].min()), 3), round(float(depth_gt[valid_mask].max()), 3)],
            "pred_range": [round(float(pred_aligned[valid_mask].min()), 3), round(float(pred_aligned[valid_mask].max()), 3)],
            "metrics": {
                "rmse": float(rec["metrics"]["rmse"]),
                "mae": float(rec["metrics"]["mae"]),
                "abs_rel": float(rec["metrics"]["abs_rel"]),
                "sq_rel": float(rec["metrics"]["sq_rel"]),
                "delta1": float(rec["metrics"]["delta1"]),
                "delta2": float(rec["metrics"]["delta2"]),
                "delta3": float(rec["metrics"]["delta3"]),
                "spearman": float(rec["metrics"]["spearman"]),
                "threshold": float(rec["threshold"]),
                "total_regions": len(regions_list)
            },
            "alignment": {
                "scale": float(scale),
                "shift": float(shift),
                "space": "inverse_depth",
                "formula": "1 / (scale * P_raw + shift)"
            },
            "images": {
                "rgb": array_to_base64_jpeg(rgb_bgr, quality=88),
                "depth_gt": array_to_base64_jpeg(depth_gt_bgr, quality=85),
                "depth_pred": array_to_base64_jpeg(depth_pred_bgr, quality=85),
                "error_map": array_to_base64_jpeg(error_bgr, quality=85)
            },
            "raw_depth": {
                "gt_b64_uint16": gt_b64_uint16,
                "pred_b64_uint16": pred_b64_uint16,
                "unit": "millimeter",
                "scale_factor": 1000.0
            },
            "mesh_3d": {
                "grid_w": 80,
                "grid_h": 60,
                "depth_gt": mesh_gt,
                "depth_pred": mesh_pred,
                "rgb_colors": mesh_rgb
            },
            "feature_maps": feature_maps,
            "regions": regions_list
        }
        scenes_output.append(scene_entry)
        print(f"Processed {sid}: {len(regions_list)} failure regions and authentic feature maps.")

    payload = {
        "version": "2.0",
        "timestamp": "2026-10-26",
        "dataset": {
            "name": "NYU Depth V2 (Official Labeled Benchmark)",
            "sensor": "Microsoft Kinect RGB-D structured-light sensor",
            "resolution": "480x640",
            "units": "meters",
            "split": "Test Split (244 scene-disjoint scenes)"
        },
        "model": {
            "name": "Depth Anything V2 (ViT-Small)",
            "encoder": "DINOv2 ViT-Small (12 Transformer Blocks, Patch Size 14x14)",
            "decoder": "DPT (Dense Prediction Transformer) with Multi-Scale RefineNet",
            "checkpoint": "depth_anything_v2_metric_hypersim_vits.pth",
            "max_depth": 20.0,
            "patch_size": 14
        },
        "scenes": scenes_output,
        "taxonomy": [
            {
                "id": "textureless",
                "label": "Textureless Surface",
                "metric_name": "Texture Variance",
                "formula": "Var(Gray) < 200.0",
                "desc": "Featureless planar walls, doors, ceilings with low gradient variance. Self-attention patches lack contrast gradients, defaulting to an ambiguous flat depth prior.",
                "remedy": "Enforce normal-guided planar consistency loss and CutBlur synthetic frequency noise augmentation."
            },
            {
                "id": "boundary_mixing",
                "label": "Boundary Mixing / Bleed",
                "metric_name": "Edge Density",
                "formula": "EdgeDensity > 0.15",
                "desc": "Depth bleeding across high-frequency foreground/background object contours. The 14x14 ViT patch blends near and far depth into a single spatial token.",
                "remedy": "Apply boundary-localized bilateral smoothing and edge-aware cross-attention filtering."
            },
            {
                "id": "occlusion",
                "label": "Occlusion Boundary",
                "metric_name": "Depth Discontinuity",
                "formula": "Delta(Depth) > 0.50m",
                "desc": "Sharp depth step discontinuities behind occluding foreground geometry where visibility is partially masked.",
                "remedy": "Incorporate multi-view temporal consensus or depth-discontinuity ranking loss."
            },
            {
                "id": "reflection",
                "label": "Specular Reflection",
                "metric_name": "Highlight Ratio",
                "formula": "V > 200 & S < 40 (Highlight Ratio > 0.10)",
                "desc": "Non-Lambertian glares, mirrors, or glossy floor reflections violating the diffuse surface assumption.",
                "remedy": "Supervise with surface normal consistency and polarization cues to discard specular false virtual depths."
            },
            {
                "id": "thin_object",
                "label": "Thin Slender Structure",
                "metric_name": "Aspect Ratio",
                "formula": "AspectRatio > 3.0 & Width < 8px",
                "desc": "Elongated geometries (chair legs, cords, poles) smaller than the ViT 14x14 receptive field, causing loss of detection.",
                "remedy": "Deploy high-resolution multi-scale feature pyamids with dilated convolutions in the decoder."
            },
            {
                "id": "poor_lighting",
                "label": "Poor / Extreme Lighting",
                "metric_name": "Brightness & Contrast",
                "formula": "Brightness < 60 | Brightness > 210",
                "desc": "Extreme underexposed shadow regions or overexposed glares depressing the visual signal-to-noise ratio.",
                "remedy": "Apply high-dynamic-range (HDR) gamma exposure augmentation during model fine-tuning."
            },
            {
                "id": "ambiguous",
                "label": "Ambiguous / Multi-Factor",
                "metric_name": "Score Margin",
                "formula": "TopScore < 0.40 | Margin < 0.10",
                "desc": "Weak overall signal or competing hypotheses where multiple visual and architectural factors contribute equally.",
                "remedy": "Perform controlled active sensor ablation to decouple lighting from surface texture effects."
            }
        ]
    }

    # The pages load the payload as a script that sets window.VEO_DATA
    out_js.parent.mkdir(parents=True, exist_ok=True)
    out_js.write_text(f"window.VEO_DATA = {json.dumps(payload)};", encoding="utf-8")

    print("\n[OK] Generated site data file at:")
    print(f"     {out_js.resolve()} (Size: {out_js.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()

