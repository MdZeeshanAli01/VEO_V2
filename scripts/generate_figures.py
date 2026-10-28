import json
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

# Set academic font style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

out_dir = Path("figures")
out_dir.mkdir(exist_ok=True)
ALIGNMENT_ABLATION = Path("outputs/alignment_ablation_full/test/alignment_ablation.json")


def load_alignment_scales(path=ALIGNMENT_ABLATION):
    """Per-scene fitted scales from `veo compare-alignment`, or None if the file is absent."""
    if not path.exists():
        return None
    records = json.loads(path.read_text(encoding="utf-8"))["records"]
    direct = np.array([r["protocols"]["direct_depth_scale_shift"]["alignment"]["scale"] for r in records])
    inverse = np.array([r["protocols"]["inverse_depth_scale_shift"]["alignment"]["scale"] for r in records])
    return direct, inverse

# ==============================================================================
# FIGURE 1: VEO Modular Architecture Diagram
# ==============================================================================
def generate_fig1_architecture():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    # Color Palette (Publication Grade)
    c_bg = '#F8FAFC'
    c_card = '#FFFFFF'
    c_primary = '#1E3A8A'     # Deep Navy
    c_m1 = '#0369A1'          # Sky Blue
    c_m2 = '#0D9488'          # Teal
    c_m3 = '#D97706'          # Amber
    c_m4 = '#7C3AED'          # Purple
    c_m5 = '#B91C1C'          # Crimson
    c_downstream = '#047857'  # Emerald

    # Main canvas background
    fig.patch.set_facecolor(c_bg)

    # Title Banner
    ax.text(8.0, 9.15, "Vision Error Observatory (VEO): Modular Diagnostic Architecture", 
            fontsize=18, fontweight='bold', color=c_primary, ha='center', va='center')
    ax.text(8.0, 8.82, "End-to-End Post-Hoc Diagnostic Pipeline for Failure Localization and Root-Cause Attribution in Monocular Depth Estimation", 
            fontsize=10.5, color='#475569', ha='center', va='center', style='italic')

    # Helper function to draw rounded box
    def draw_box(x, y, w, h, bg, border, title, title_color='#FFFFFF', corner=0.25):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={corner}", 
                                      facecolor=bg, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        # Header banner inside box
        header_h = 0.55
        header_rect = patches.FancyBboxPatch((x, y + h - header_h), w, header_h, 
                                             boxstyle=f"round,pad=0,rounding_size={corner}",
                                             facecolor=border, edgecolor=border, linewidth=1, zorder=3)
        ax.add_patch(header_rect)
        # Rect cover bottom corners of header
        rect_cover = patches.Rectangle((x, y + h - header_h), w, 0.2, facecolor=border, edgecolor=border, zorder=3)
        ax.add_patch(rect_cover)
        ax.text(x + w/2, y + h - header_h/2, title, fontsize=10.5, fontweight='bold', 
                color=title_color, ha='center', va='center', zorder=4)

    # 1. INPUT STAGE (Column 1)
    draw_box(0.5, 3.8, 2.3, 4.6, c_card, '#475569', "INPUT DATA (RGB-D)")
    ax.text(1.65, 7.8, "RGB Image", fontsize=10, fontweight='bold', color='#1E293B', ha='center')
    ax.text(1.65, 7.55, r"$I \in \mathbb{R}^{H \times W \times 3}$", fontsize=9, color='#64748B', ha='center')
    
    ax.text(1.65, 6.7, "Pretrained Model\nRaw Output", fontsize=10, fontweight='bold', color='#1E293B', ha='center')
    ax.text(1.65, 6.25, r"$P \in \mathbb{R}^{H \times W}$ (relative/disp)", fontsize=8.5, color='#64748B', ha='center')

    ax.text(1.65, 5.3, "Ground Truth\nMetric Depth", fontsize=10, fontweight='bold', color='#1E293B', ha='center')
    ax.text(1.65, 4.85, r"$D_{gt} \in [0.7\mathrm{m}, 10.0\mathrm{m}]$", fontsize=8.5, color='#64748B', ha='center')

    ax.text(1.65, 4.2, "[NYU Depth V2 / Hypersim]", fontsize=8, color='#0284C7', ha='center', style='italic')

    # Arrow 0 -> M1
    ax.annotate("", xy=(3.2, 6.1), xytext=(2.8, 6.1),
                arrowprops={'arrowstyle': "->", 'color': '#334155', 'lw': 2})

    # 2. MODULE M1: Scale-Shift Depth Alignment (Column 2)
    draw_box(3.2, 3.8, 2.7, 4.6, c_card, c_m1, "M1: SCALE-SHIFT ALIGNMENT")
    ax.text(4.55, 7.8, "Inverse-Depth OLS Fitting", fontsize=9.5, fontweight='bold', color=c_m1, ha='center')
    ax.text(4.55, 7.35, r"$\arg\min_{s,b} \sum_{i,j} \left(sP_{ij} + b - \frac{1}{D_{ij}}\right)^2$", fontsize=8.5, color='#0F172A', ha='center')
    
    # Polar reversal notice
    rect_polar = patches.Rectangle((3.4, 6.2), 2.3, 0.9, facecolor='#EFF6FF', edgecolor='#BFDBFE', zorder=3)
    ax.add_patch(rect_polar)
    ax.text(4.55, 6.75, "Fit in Disparity Space", fontsize=8.5, fontweight='bold', color='#1D4ED8', ha='center', zorder=4)
    ax.text(4.55, 6.4, r"$s > 0$ observed (244/244)", fontsize=8, color='#1E40AF', ha='center', zorder=4)

    ax.text(4.55, 5.65, "Metric Reconstruction", fontsize=9.5, fontweight='bold', color=c_m1, ha='center')
    ax.text(4.55, 5.25, r"$\hat{D}_{ij} = \frac{1}{\max(s P_{ij} + b, 10^{-6})}$", fontsize=9, color='#0F172A', ha='center')
    ax.text(4.55, 4.4, "Metric Checkpoints (Hypersim):\n$s=1, b=0$ (Identity)", fontsize=8, color='#475569', ha='center')

    # Arrow M1 -> M2
    ax.annotate("", xy=(6.3, 6.1), xytext=(5.9, 6.1),
                arrowprops={'arrowstyle': "->", 'color': '#334155', 'lw': 2})

    # 3. MODULE M2: Dense Error Computation (Column 3)
    draw_box(6.3, 3.8, 2.7, 4.6, c_card, c_m2, "M2: DENSE ERROR MAPS")
    ax.text(7.65, 7.8, "Residual Calculation", fontsize=9.5, fontweight='bold', color=c_m2, ha='center')
    ax.text(7.65, 7.4, r"Absolute: $| \hat{D}_{ij} - D_{ij} |$", fontsize=8.5, color='#0F172A', ha='center')
    ax.text(7.65, 7.0, r"Relative: $E_{ij} = \frac{|\hat{D}_{ij} - D_{ij}|}{D_{ij}}$", fontsize=9, color='#0F172A', ha='center')

    # Baseline metrics box
    rect_bench = patches.Rectangle((6.5, 4.5), 2.3, 2.1, facecolor='#F0FDF4', edgecolor='#BBF7D0', zorder=3)
    ax.add_patch(rect_bench)
    ax.text(7.65, 6.35, "Global Baseline Metrics", fontsize=9, fontweight='bold', color='#15803D', ha='center', zorder=4)
    ax.text(7.65, 5.95, r"• RMSE, MAE, AbsRel, SqRel", fontsize=8, color='#166534', ha='center', zorder=4)
    ax.text(7.65, 5.6, r"• Threshold Accuracy $\delta_1, \delta_2, \delta_3$", fontsize=8, color='#166534', ha='center', zorder=4)
    ax.text(7.65, 5.25, r"• Spearman Rank Correlation", fontsize=8, color='#166534', ha='center', zorder=4)
    ax.text(7.65, 4.8, r"DA-V2: AbsRel = 0.1040, $\delta_1$=89.7%", fontsize=8, fontweight='bold', color='#14532D', ha='center', zorder=4)

    # Arrow M2 -> M3
    ax.annotate("", xy=(9.4, 6.1), xytext=(9.0, 6.1),
                arrowprops={'arrowstyle': "->", 'color': '#334155', 'lw': 2})

    # 4. MODULE M3: Spatial Region Segmentation (Column 4)
    draw_box(9.4, 3.8, 2.9, 4.6, c_card, c_m3, "M3: REGION SEGMENTATION")
    ax.text(10.85, 7.8, "Adaptive Error Thresholding", fontsize=9.5, fontweight='bold', color=c_m3, ha='center')
    ax.text(10.85, 7.4, r"$\tau = \mathrm{Percentile}(E_{valid}, 85.0)$", fontsize=8.5, color='#0F172A', ha='center')
    ax.text(10.85, 7.0, r"High-Error Mask: $B_{ij} = (E_{ij} > \tau)$", fontsize=8.5, color='#0F172A', ha='center')

    # Morphological segmentation
    rect_cc = patches.Rectangle((9.6, 4.4), 2.5, 2.2, facecolor='#FFFBEB', edgecolor='#FDE68A', zorder=3)
    ax.add_patch(rect_cc)
    ax.text(10.85, 6.35, "Connected Components", fontsize=9, fontweight='bold', color='#B45309', ha='center', zorder=4)
    ax.text(10.85, 5.95, "• 8-Connectivity Labeling", fontsize=8, color='#92400E', ha='center', zorder=4)
    ax.text(10.85, 5.6, "• Spatial Cluster Filtering:", fontsize=8, color='#92400E', ha='center', zorder=4)
    ax.text(10.85, 5.25, r"Prune Noise Area $< 25$ pixels", fontsize=8, color='#B45309', ha='center', zorder=4)
    ax.text(10.85, 4.85, "Yields K Disjoint Failure Regions:", fontsize=8, color='#92400E', ha='center', zorder=4)
    ax.text(10.85, 4.55, r"$\mathcal{R} = \{R_1, R_2, \dots, R_K\}$ (5,236 total)", fontsize=8, fontweight='bold', color='#78350F', ha='center', zorder=4)

    # Arrow M3 -> M4
    ax.annotate("", xy=(12.7, 6.1), xytext=(12.3, 6.1),
                arrowprops={'arrowstyle': "->", 'color': '#334155', 'lw': 2})

    # 5. MODULE M4: Multi-Signal Evidence Extraction (Column 5)
    draw_box(12.7, 3.8, 2.8, 4.6, c_card, c_m4, "M4: EVIDENCE EXTRACTION")
    ax.text(14.1, 7.8, "7 Multi-Signal Evidence", fontsize=9.5, fontweight='bold', color=c_m4, ha='center')

    features = [
        ("1. Texture Variance", r"$\mathrm{Var}(I_{gray}(R_k))$"),
        ("2. Canny Edge Density", r"$\mu(\mathrm{Canny}(R_k))/255$"),
        ("3. Mean Luminance", r"$\mu(I_{gray}(R_k)) \in [0, 255]$"),
        ("4. Local Contrast", r"$\sigma(I_{gray}(R_k))$"),
        ("5. Specular Highlights", "Frac(V > 200 & S < 40)"),
        ("6. Bounding Box AR", r"$\max(w,h) / \min(w,h)$"),
        ("7. Depth Discontinuity", r"$\|\nabla D_{gt}\|$ on $\partial R_k$"),
    ]
    for idx, (f_name, f_eq) in enumerate(features):
        yy = 7.35 - idx * 0.46
        ax.text(12.9, yy, f_name, fontsize=7.5, fontweight='bold', color='#1E293B', ha='left')
        ax.text(15.3, yy, f_eq, fontsize=7.2, color='#6D28D9', ha='right')

    # Arrow from M4 down to M5
    ax.annotate("", xy=(14.1, 3.2), xytext=(14.1, 3.8),
                arrowprops={'arrowstyle': "->", 'color': '#334155', 'lw': 2})

    # 6. MODULE M5: Rule-Based Cause Attribution & Ambiguity Gate (Bottom Row - Wide Card)
    draw_box(2.0, 0.4, 8.5, 2.8, c_card, c_m5, "M5: RULE-BASED ATTRIBUTION & AMBIGUITY GATE")

    # Left column of M5: Normalized Scoring Functions
    ax.text(4.0, 2.7, "Hand-Set Rule-Based Scores", fontsize=9, fontweight='bold', color=c_m5, ha='center')
    rules = [
        r"$\bullet\ \mathrm{score}_{\mathrm{textureless}} = \mathrm{clip}(1.0 - \mathrm{texture\_var} / 500.0, 0, 1)$",
        r"$\bullet\ \mathrm{score}_{\mathrm{boundary}} = \mathrm{clip}(\mathrm{edge\_density} \times 3.0, 0, 1)$",
        r"$\bullet\ \mathrm{score}_{\mathrm{lighting}} = \mathrm{clip}(1.0 - \mathrm{contrast} / 60.0, 0, 1)\ \mathrm{if}\ (B < 60\ \mathrm{or}\ B > 200)$",
        r"$\bullet\ \mathrm{score}_{\mathrm{thin}} = \mathrm{clip}((\mathrm{aspect\_ratio} - 3.0) / 5.0, 0, 1)$",
        r"$\bullet\ \mathrm{score}_{\mathrm{reflection}} = \mathrm{clip}(\mathrm{highlight\_ratio} \times 5.0, 0, 1)$",
        r"$\bullet\ \mathrm{score}_{\mathrm{occlusion}} = \mathrm{clip}(\mathrm{depth\_discontinuity} / 1.0, 0, 1)$",
    ]
    for idx, r_str in enumerate(rules):
        ax.text(2.2, 2.35 - idx * 0.32, r_str, fontsize=7.5, color='#1E293B', ha='left')

    # Right column of M5: Fixed-threshold ambiguity gate
    rect_gate = patches.Rectangle((6.8, 0.55), 3.5, 2.0, facecolor='#FEF2F2', edgecolor='#FECACA', zorder=3)
    ax.add_patch(rect_gate)
    ax.text(8.55, 2.35, "Fixed-Threshold Ambiguity Gate", fontsize=9, fontweight='bold', color='#991B1B', ha='center', zorder=4)
    ax.text(8.55, 2.05, r"Leading Scores: $s_{(1)} \geq s_{(2)}$", fontsize=8, color='#7F1D1D', ha='center', zorder=4)
    ax.text(8.55, 1.75, r"Condition: $s_{(1)} < 0.40\ \mathrm{or}\ (s_{(1)} - s_{(2)} < 0.10)$", fontsize=7.8, fontweight='bold', color='#B91C1C', ha='center', zorder=4)
    ax.text(8.55, 1.4, "True -> Ambiguous (Prevents False Certainty)", fontsize=7.5, color='#991B1B', ha='center', zorder=4)
    ax.text(8.55, 1.1, "False -> Top Category (High/Medium Conf)", fontsize=7.5, color='#15803D', ha='center', zorder=4)
    ax.text(8.55, 0.75, "7 Classes: textureless, boundary, thin, etc.", fontsize=7.2, color='#475569', ha='center', zorder=4)

    # 7. DOWNSTREAM APPLICATIONS (Bottom Right)
    draw_box(11.0, 0.4, 4.5, 2.8, c_card, c_downstream, "V1 EVALUATIONS")
    ax.text(13.25, 2.7, "Reported with limitations", fontsize=9, fontweight='bold', color=c_downstream, ha='center')

    down_items = [
        "1. Diagnostic Scene Cards & Spatial Heatmaps",
        "2. Cross-Model Label Shares (exploratory)",
        "3. Human Agreement, N=50 (kappa = 0.26 / 0.14)",
        "4. Scoring-Function Sanity Check",
        "5. Oracle Boundary Filtering (-0.35% AbsRel, GT masks)",
    ]
    for idx, d_str in enumerate(down_items):
        ax.text(11.2, 2.3 - idx * 0.35, d_str, fontsize=8, color='#065F46', ha='left')

    # Arrow from M5 to Downstream
    ax.annotate("", xy=(11.0, 1.8), xytext=(10.5, 1.8),
                arrowprops={'arrowstyle': "->", 'color': '#334155', 'lw': 2})

    # Figure Note on AI Generation (Required by User)
    ax.text(8.0, 0.1, "[Note: Architecture diagram generated using AI visualization tools]", 
            fontsize=8, color='#64748B', ha='center', va='center', style='italic')

    fig_path = out_dir / "fig1_veo_architecture.png"
    plt.savefig(fig_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved Fig 1: {fig_path}")

# ==============================================================================
# FIGURE 2: Polarity Reversal & Cross-Model Failure Fingerprints
# ==============================================================================
def generate_fig2_polarity_and_fingerprints():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Subplot A: fitted scale per test scene. Plot measured values only; never synthesize them.
    scales = load_alignment_scales()
    if scales is not None:
        direct_scales, inverse_scales = scales
        scenes = np.arange(1, len(direct_scales) + 1)
        n_neg = int((direct_scales < 0).sum())
        n_pos = int((inverse_scales > 0).sum())
        ax1.axhline(0, color='black', linestyle='--', linewidth=1.2, alpha=0.7)
        ax1.scatter(scenes, direct_scales, color='#DC2626', alpha=0.6, s=18,
                    label=f'Direct depth fit (s < 0: {n_neg}/{len(scenes)})')
        ax1.scatter(scenes, inverse_scales, color='#2563EB', alpha=0.6, s=18,
                    label=f'Inverse-depth fit (s > 0: {n_pos}/{len(scenes)})')
        ax1.set_title(f"(a) Fitted Scale $s$ Across {len(scenes)} NYU Test Scenes", fontsize=11, fontweight='bold', pad=10)
        ax1.set_xlabel("Test Scene Index", fontsize=10)
        ax1.set_ylabel("Fitted Scale Parameter ($s$)", fontsize=10)
        ax1.legend(loc='best', fontsize=8.5, framealpha=0.9)
    else:
        # Per-scene values unavailable: show only the reported sign counts, labelled as such
        ax1.bar([0, 1], [244, 244], color=['#DC2626', '#2563EB'], width=0.5)
        ax1.set_xticks([0, 1])
        ax1.set_xticklabels(['Direct depth fit\ns < 0', 'Inverse-depth fit\ns > 0'], fontsize=9.5)
        ax1.set_ylabel("Test scenes (of 244)", fontsize=10)
        ax1.set_ylim(0, 290)
        ax1.set_title("(a) Sign of Fitted Scale (reported counts)", fontsize=11, fontweight='bold', pad=10)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Subplot B: Cross-Model Failure Fingerprinting
    categories = ['Ambiguous', 'Textureless', 'Boundary', 'Reflection', 'Poor Lighting', 'Thin Object', 'Occlusion']
    da_v2_pct = [39.3, 19.5, 18.0, 13.1, 6.7, 2.9, 0.4]
    dpt_midas_pct = [39.1, 17.3, 15.0, 17.4, 7.8, 2.6, 0.8]

    x = np.arange(len(categories))
    width = 0.35

    rects1 = ax2.bar(x - width/2, da_v2_pct, width, label='Depth Anything V2 Small (5,236 regions)', color='#3B82F6', edgecolor='#1D4ED8')
    rects2 = ax2.bar(x + width/2, dpt_midas_pct, width, label='DPT-Hybrid-MiDaS (3,689 regions)', color='#F59E0B', edgecolor='#D97706')

    ax2.set_title("(b) Share of Regions per VEO Label (%), Exploratory", fontsize=11, fontweight='bold', pad=10)
    ax2.set_ylabel("Share of Each Model's Regions (%)", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=25, ha='right', fontsize=9)
    ax2.set_ylim(0, 48)
    ax2.grid(True, axis='y', linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', fontsize=8.5, framealpha=0.9)

    # Add data labels above bars
    for rect in rects1:
        height = rect.get_height()
        ax2.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2), textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, color='#1E3A8A')
        
    for rect in rects2:
        height = rect.get_height()
        ax2.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2), textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, color='#78350F')

    plt.tight_layout()
    fig_path = out_dir / "fig2_polarity_and_fingerprints.png"
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved Fig 2: {fig_path}")

# ==============================================================================
# FIGURE 3: Controlled Intervention & Downstream Refinement
# ==============================================================================
def generate_fig3_intervention_and_downstream():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.0), dpi=300)

    # Subplot A: Scoring-function sanity check (Scene 0049 Region 8); the depth model is not re-run
    stages = ['Original Wall Patch\n(High-Error)', 'Synthetic Texture\nInjected (+Noise)']
    variance_vals = [176.82, 689.39]
    score_vals = [0.6464, 0.0000]

    color_var = '#0284C7'
    color_score = '#DC2626'

    ax1_twin = ax1.twinx()
    w = 0.28
    x_pos = np.arange(len(stages))

    ax1.bar(x_pos - w/2, variance_vals, width=w, color=color_var, label='Texture Variance (Var(I))', edgecolor='#0369A1')
    ax1_twin.bar(x_pos + w/2, score_vals, width=w, color=color_score, label='Textureless Heuristic Score', edgecolor='#991B1B')

    ax1.set_title("(a) Scoring Sanity Check: Added Noise (scene_0049, Region 8)", fontsize=11, fontweight='bold', pad=10)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(stages, fontsize=9.5)
    ax1.set_ylabel("Grayscale Texture Variance", color=color_var, fontsize=10)
    ax1_twin.set_ylabel("Textureless Evidence Score [0, 1]", color=color_score, fontsize=10)
    ax1.set_ylim(0, 800)
    ax1_twin.set_ylim(0, 1.0)
    ax1.grid(True, linestyle=':', alpha=0.5)

    ax1.annotate("Diagnosis: textureless\n(Conf: High)", xy=(0, 200), xytext=(0, 360),
                ha='center', fontsize=8.5, fontweight='bold', color='#1E293B',
                bbox={'boxstyle': "round,pad=0.3", 'fc': "#F1F5F9", 'ec': "#CBD5E1"})

    ax1.annotate("Diagnosis: ambiguous\n(Score Collapsed to 0.0)", xy=(1, 400), xytext=(1, 550),
                ha='center', fontsize=8.5, fontweight='bold', color='#991B1B',
                bbox={'boxstyle': "round,pad=0.3", 'fc': "#FEF2F2", 'ec': "#FECACA"})

    # Subplot B: Downstream Refinement Across 207 Boundary Scenes
    metrics = ['Regional Boundary RMSE (m)', 'Regional Boundary AbsRel', 'Global Scene RMSE (m)']
    baseline_scores = [0.6629, 0.2348, 0.4658]
    refined_scores = [0.6618, 0.2340, 0.4658]

    x2 = np.arange(len(metrics))
    w2 = 0.35

    ax2.bar(x2 - w2/2, baseline_scores, width=w2, label='Baseline Depth Anything V2', color='#64748B', edgecolor='#334155')
    ax2.bar(x2 + w2/2, refined_scores, width=w2, label='Bilateral Filtering in GT-Selected Masks', color='#10B981', edgecolor='#059669')

    ax2.set_title("(b) Oracle Boundary Filtering on 207 Test Scenes (GT masks)", fontsize=11, fontweight='bold', pad=10)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(metrics, fontsize=9)
    ax2.set_ylabel("Error Metric Magnitude", fontsize=10)
    ax2.set_ylim(0, 0.8)
    ax2.grid(True, axis='y', linestyle=':', alpha=0.5)
    ax2.legend(loc='upper right', fontsize=8.5)

    # Improvement percentage badges
    ax2.annotate("Δ: -0.16%\n(RMSE ↓)", xy=(0, 0.67), xytext=(0, 0.72),
                ha='center', fontsize=8, fontweight='bold', color='#065F46',
                bbox={'boxstyle': "round,pad=0.2", 'fc': "#ECFDF5", 'ec': "#A7F3D0"})
    
    ax2.annotate("Δ: -0.35%\n(AbsRel ↓)", xy=(1, 0.24), xytext=(1, 0.31),
                ha='center', fontsize=8, fontweight='bold', color='#065F46',
                bbox={'boxstyle': "round,pad=0.2", 'fc': "#ECFDF5", 'ec': "#A7F3D0"})

    ax2.annotate("Δ: +0.00%\n(No Distortion)", xy=(2, 0.47), xytext=(2, 0.54),
                ha='center', fontsize=8, fontweight='bold', color='#1E293B',
                bbox={'boxstyle': "round,pad=0.2", 'fc': "#F8FAFC", 'ec': "#E2E8F0"})

    plt.tight_layout()
    fig_path = out_dir / "fig3_intervention_and_downstream.png"
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved Fig 3: {fig_path}")

if __name__ == "__main__":
    generate_fig1_architecture()
    generate_fig2_polarity_and_fingerprints()
    generate_fig3_intervention_and_downstream()
    print("\nAll 3 publication figures generated successfully!")
