import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_slide_image(width, height, bg_color, header_bg, title, subtitle, bullets, callout=None, footer="Vision Error Observatory (VEO) - Capstone Research"):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Header banner
    draw.rectangle([(0, 0), (width, 110)], fill=header_bg)
    
    # Try system fonts, fall back to default
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_sub = ImageFont.truetype("ariali.ttf", 20)
        font_body = ImageFont.truetype("arial.ttf", 22)
        font_body_b = ImageFont.truetype("arialbd.ttf", 22)
        font_callout = ImageFont.truetype("arialbd.ttf", 20)
        font_footer = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_body = font_title
        font_body_b = font_title
        font_callout = font_title
        font_footer = font_title

    # Title & Subtitle
    draw.text((40, 25), title, fill=(255, 255, 255), font=font_title)
    draw.text((42, 70), subtitle, fill=(210, 230, 255), font=font_sub)

    # Bullets
    y_pos = 145
    for b_bold, b_text in bullets:
        # bullet circle
        draw.ellipse([(45, y_pos + 6), (57, y_pos + 18)], fill=header_bg)
        draw.text((70, y_pos), b_bold, fill=(20, 35, 60), font=font_body_b)
        x_offset = draw.textlength(b_bold + " ", font=font_body_b) if hasattr(draw, 'textlength') else 200
        draw.text((70 + x_offset, y_pos), b_text, fill=(50, 65, 85), font=font_body)
        y_pos += 48

    # Callout Box if present
    if callout:
        c_title, c_text, c_border, c_bg = callout
        box_y1 = y_pos + 15
        box_y2 = height - 60
        draw.rounded_rectangle([(40, box_y1), (width - 40, box_y2)], radius=12, fill=c_bg, outline=c_border, width=2)
        draw.text((65, box_y1 + 20), c_title, fill=c_border, font=font_callout)
        draw.text((65, box_y1 + 55), c_text, fill=(40, 50, 65), font=font_body)

    # Footer
    draw.line([(0, height - 40), (width, height - 40)], fill=(220, 225, 235), width=1)
    draw.text((40, height - 30), footer, fill=(120, 135, 150), font=font_footer)

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def main():
    out_dir = Path("web_app")
    out_dir.mkdir(exist_ok=True)
    video_path = out_dir / "veo_explainer.mp4"
    outputs_path = Path("outputs") / "veo_explainer_video.mp4"

    width, height = 1280, 720
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))

    if not writer.isOpened():
        print("Error: Could not open VideoWriter.")
        return

    # Color themes
    c_blue = (15, 45, 95)
    c_red = (150, 25, 25)
    c_amber = (180, 95, 10)
    c_green = (15, 105, 65)

    slides_config = [
        # Slide 1: The Leaderboard Illusion
        {
            "header_bg": c_blue,
            "title": "SCENE 1: THE LEADERBOARD ILLUSION",
            "subtitle": "Why Standard Benchmark Metrics (AbsRel = 0.10) Obscure Critical Model Failures",
            "bullets": [
                ("The Leaderboard Claim:", "Depth Anything V2 achieves an impressive 0.1040 AbsRel and 89.7% delta1."),
                ("The Statistical Flaw:", "Global scalars collapse millions of 3D pixel errors into a single monolithic average."),
                ("The Hidden Hazard:", "Catastrophic localized failures on glass, thin legs, and flat walls are completely concealed."),
                ("The Deployment Risk:", "Autonomous robots and AR systems crash because models misjudge local obstacles by 2+ meters.")
            ],
            "callout": (
                "THE PROBLEM:",
                "A model can achieve a top leaderboard ranking while having localized 3-meter depth errors on obstacles.",
                c_red, (255, 240, 240)
            ),
            "duration_sec": 7
        },
        # Slide 2: The Critical Gaps
        {
            "header_bg": c_red,
            "title": "SCENE 2: THE CRITICAL OBSERVABILITY GAP",
            "subtitle": "What Current Computer Vision Tools Fail to Tell You",
            "bullets": [
                ("Traditional Metrics (RMSE / MAE):", "Give only scalar scores — they cannot answer WHERE or WHY a model failed."),
                ("Feature Saliency (Grad-CAM / RISE):", "Highlight internal neural activations, NOT physical geometric failure causes."),
                ("The Polarity Reversal Trap:", "Naive direct regression inverts physical 3D geometry (s < 0 in 244/244 test scenes)."),
                ("Black-Box Diagnosis:", "Dense error localization is rarely paired with interpretable, per-region cause hypotheses.")
            ],
            "callout": (
                "THE RESEARCH GAP:",
                "We need an external, post-hoc 'Observatory' that audits depth models like an MRI scanner—diagnosing root causes.",
                c_blue, (240, 245, 255)
            ),
            "duration_sec": 7
        },
        # Slide 3: The VEO Paradigm & 5 Modules
        {
            "header_bg": c_amber,
            "title": "SCENE 3: THE VISION ERROR OBSERVATORY (VEO)",
            "subtitle": "A Model-Agnostic 5-Stage Diagnostic & Observability Framework",
            "bullets": [
                ("Module M1 (Inverse Alignment):", "Fits scale-shift in 1/D space, matching disparity output (s > 0 in 244/244 scenes)."),
                ("Module M2 (Dense Error Maps):", "Computes dense relative residuals |D_pred - D_gt| / D_gt across all valid metric pixels."),
                ("Module M3 (Region Segmentation):", "Adaptive 85th-percentile error thresholding with 8-connectivity morphological clustering."),
                ("Module M4 (7 Evidence Signals):", "Extracts Texture Variance, Canny Edge Density, Brightness, Contrast, Highlights, AR, and Discontinuity."),
                ("Module M5 (Cause Attribution):", "Hand-set rule-based scores with an ambiguity gate (abstain if top < 0.40 or margin < 0.10).")
            ],
            "callout": (
                "THE VEO SOLUTION:",
                "VEO isolates structured error clusters and attributes them to 7 physical categories: textureless, boundary, reflection, etc.",
                c_green, (240, 253, 245)
            ),
            "duration_sec": 8
        },
        # Slide 4: Empirical Validation Proofs
        {
            "header_bg": c_green,
            "title": "SCENE 4: V1 RESULTS AND LIMITATIONS",
            "subtitle": "244 NYU Depth V2 Test Images (custom scene-disjoint split)",
            "bullets": [
                ("Human Agreement (N=50):", "kappa vs VEO = 0.26 / 0.14, accuracy 36%; inter-rater kappa = 0.35."),
                ("Where VEO Commits (29/50):", "58.6% accuracy vs 41.4% majority baseline. Textureless 7/8 correct, reflection 0/7."),
                ("Scoring Sanity Check:", "Adding noise drops the textureless score 0.646 -> 0.000; checks the formula, not the model."),
                ("Oracle Boundary Filtering:", "-0.35% regional AbsRel over 207 scenes, using ground-truth masks (not deployable).")
            ],
            "callout": (
                "WORK IN PROGRESS:",
                "VEO's localization works; its cause labels need calibration and larger validation (v2 in progress).",
                c_blue, (240, 245, 255)
            ),
            "duration_sec": 7
        },
        # Slide 5: Welcome to the Interactive Lab
        {
            "header_bg": c_blue,
            "title": "SCENE 5: WELCOME TO THE INTERACTIVE DIAGNOSTIC LAB",
            "subtitle": "Explore Live Test Scenes, Click High-Error Regions, and Inspect Mathematical Formulas",
            "bullets": [
                ("Step 1 (Select a Scene):", "Choose from NYU Depth V2 test scenes (Office, Living Room, Hallway)."),
                ("Step 2 (View 4 Synchronized Views):", "Compare RGB Image, Depth Anything V2 Output, Ground Truth Depth, and Error Heatmaps."),
                ("Step 3 (Click Any Error Region):", "Isolate bounding boxes, zoom into crops, and inspect all 7 extracted visual evidence signals."),
                ("Step 4 (Inspect Real-Time Math):", "Watch the heuristic formulas calculate scores and trigger the ambiguity gate live."),
                ("Step 5 (Edit the Evidence):", "Click 'Inject Synthetic Texture' to see how the rule-based scores respond.")
            ],
            "callout": (
                "READY TO EXPLORE:",
                "Switch to the 'Interactive Diagnostic Observatory' tab below to begin hands-on model failure analysis!",
                c_amber, (255, 250, 235)
            ),
            "duration_sec": 6
        }
    ]

    print("Generating VEO Explainer Video (720p HD, 30 FPS)...")

    # Render frames with smooth 15-frame cross-fades
    fade_frames = 15
    prev_bgr = None

    for idx, slide in enumerate(slides_config):
        curr_bgr = create_slide_image(
            width=width, height=height,
            bg_color=(250, 252, 255),
            header_bg=slide["header_bg"],
            title=slide["title"],
            subtitle=slide["subtitle"],
            bullets=slide["bullets"],
            callout=slide["callout"]
        )

        total_frames = int(slide["duration_sec"] * fps)
        
        # If there is a previous slide, cross-fade transition
        if prev_bgr is not None:
            for f in range(fade_frames):
                alpha = f / float(fade_frames)
                blended = cv2.addWeighted(prev_bgr, 1.0 - alpha, curr_bgr, alpha, 0)
                writer.write(blended)
            steady_frames = total_frames - fade_frames
        else:
            steady_frames = total_frames

        # Steady display
        for _ in range(steady_frames):
            writer.write(curr_bgr)

        prev_bgr = curr_bgr
        print(f"  - Rendered Slide {idx + 1}/5 ({slide['duration_sec']}s)")

    writer.release()

    # Also copy to outputs
    import shutil
    outputs_path.parent.mkdir(exist_ok=True)
    shutil.copyfile(video_path, outputs_path)

    print(f"\n[OK] Explainer video successfully generated and saved to:")
    print(f"     - {video_path.resolve()}")
    print(f"     - {outputs_path.resolve()}")

if __name__ == "__main__":
    main()

