import json
from pathlib import Path

def generate_web_app_html():
    data_path = Path("web_app/data/app_data.json")
    if not data_path.exists():
        raise FileNotFoundError(f"Missing {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data_json_str = f.read()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VEO: Vision Error Observatory | Interactive Diagnostic Platform</title>
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="alternate icon" href="favicon.ico">
  <link rel="stylesheet" href="assets/css/tailwind.min.css">
  <link rel="stylesheet" href="assets/fontawesome/all.min.css">
  <script src="assets/js/chart.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #0B0F19;
      color: #E2E8F0;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    .canvas-container {{
      position: relative;
      cursor: crosshair;
      user-select: none;
    }}
    .bbox-highlight {{
      position: absolute;
      border: 2px solid #EF4444;
      background-color: rgba(239, 68, 68, 0.25);
      transition: all 0.15s ease-in-out;
      pointer-events: auto;
      cursor: pointer;
    }}
    .bbox-highlight:hover, .bbox-highlight.selected {{
      border-color: #38BDF8;
      background-color: rgba(56, 189, 248, 0.4);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.8);
      z-index: 20;
    }}
    .glow-cyan {{
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.35);
    }}
    .glow-red {{
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.35);
    }}
    .tab-btn.active {{
      background-color: #1E293B;
      color: #38BDF8;
      border-bottom: 2px solid #38BDF8;
    }}
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{ background: #0F172A; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Header Banner -->
  <header class="bg-[#0F172A] border-b border-slate-800 sticky top-0 z-50 backdrop-blur-md bg-opacity-95">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-lg bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-white shadow-lg shadow-cyan-500/20">
          <i class="fa-solid fa-cube text-xl"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-xl font-bold tracking-tight text-white">Vision Error Observatory <span class="text-cyan-400 font-mono text-sm">(VEO)</span></h1>
            <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800">Capstone Final</span>
          </div>
          <p class="text-xs text-slate-400">Diagnostic & Observability Framework for Monocular Depth Estimation | NMIMS Hyderabad</p>
        </div>
      </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Fig 1 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig1_veo_architecture.png" target="_blank">
              <img src="assets/fig1_veo_architecture.png" alt="Figure 1: VEO Pipeline Architecture" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 1: VEO Architecture</p>
            <p class="text-[11px] text-slate-400 leading-tight">Dual-stream metric inversion, connected components failure discovery, and multi-hypothesis classifier.</p>
          </div>

          <!-- Fig 2 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig2_polarity_and_fingerprints.png" target="_blank">
              <img src="assets/fig2_polarity_and_fingerprints.png" alt="Figure 2: Polarity & Fingerprints" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 2: Empirical Fingerprints</p>
            <p class="text-[11px] text-slate-400 leading-tight">Direct vs inverse scale polarity reversal distributions and distinctive per-cause multi-modal radar signatures.</p>
          </div>

          <!-- Fig 3 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig3_intervention_and_downstream.png" target="_blank">
              <img src="assets/fig3_intervention_and_downstream.png" alt="Figure 3: Downstream Boundary Refinement" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 3: Downstream Intervention</p>
            <p class="text-[11px] text-slate-400 leading-tight">Closed-loop boundary-guided bilateral filtering showing regional metric improvement without global distortion.</p>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="flex items-center space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800 text-sm">
        <button onclick="switchTab('explainer')" id="tab-explainer" class="tab-btn active px-3.5 py-1.5 rounded-lg font-medium transition flex items-center space-x-2">
          <i class="fa-solid fa-play-circle text-cyan-400"></i>
          <span>1. Concept & Video</span>
        </button>
        <button onclick="switchTab('observatory')" id="tab-observatory" class="tab-btn px-3.5 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white transition flex items-center space-x-2">
          <i class="fa-solid fa-microscope text-amber-400"></i>
          <span>2. Interactive Diagnostic Lab</span>
        </button>
        <button onclick="switchTab('benchmarks')" id="tab-benchmarks" class="tab-btn px-3.5 py-1.5 rounded-lg font-medium text-slate-400 hover:text-white transition flex items-center space-x-2">
          <i class="fa-solid fa-chart-line text-emerald-400"></i>
          <span>3. Scientific Validation</span>
        </button>
      </nav>

      <div class="flex items-center space-x-3">
        <a href="assets/VEO_conference_paper.pdf" target="_blank" class="px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 text-xs font-semibold flex items-center space-x-1.5 transition">
          <i class="fa-solid fa-file-pdf"></i>
          <span>Read Paper (PDF)</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="flex-grow max-w-7xl w-full mx-auto px-4 py-6">

    <!-- ========================================================================= -->
    <!-- TAB 1: CONCEPTUAL EXPLAINER & VIDEO STORYBOARD -->
    <!-- ========================================================================= -->
    <div id="view-explainer" class="space-y-8">
      
      <!-- Top Hero Section -->
      <div class="bg-gradient-to-r from-slate-900 via-[#131D31] to-slate-900 rounded-2xl border border-slate-800 p-6 md:p-8 shadow-2xl relative overflow-hidden">
        <div class="max-w-3xl space-y-4">
          <span class="px-3 py-1 rounded-full text-xs font-mono font-medium bg-red-950/80 text-red-300 border border-red-800/80 inline-flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
            <span>The Computer Vision Leaderboard Blind Spot</span>
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white leading-tight">
            Why High Aggregate Accuracy Hides <span class="text-transparent bg-clip-text bg-gradient-to-r from-red-400 to-amber-400">Catastrophic Failures</span>
          </h2>
          <p class="text-slate-300 leading-relaxed text-sm md:text-base">
            Modern foundation models like <strong>Depth Anything V2</strong> achieve state-of-the-art benchmark scores (AbsRel = 0.104, δ1 = 89.7%). 
            Yet on paper, standard metrics (RMSE, AbsRel) collapse millions of 3D pixels into a single average. 
            They cannot tell you <strong>WHERE</strong> a model failed, <strong>WHY</strong> it failed, or <strong>HOW</strong> to fix it. 
            In real-world robotics, a single localized 3-meter error on glass or a chair leg causes catastrophic collisions.
          </p>
          <div class="pt-2 flex flex-wrap gap-4">
            <button onclick="switchTab('observatory')" class="px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-sm shadow-lg shadow-cyan-600/30 flex items-center space-x-2 transition">
              <span>Launch Interactive Diagnosis Lab</span>
              <i class="fa-solid fa-arrow-right"></i>
            </button>
            <button onclick="playExplainerVoiceover()" id="btn-voiceover" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-sm font-medium flex items-center space-x-2 transition">
              <i class="fa-solid fa-volume-high text-cyan-400"></i>
              <span>Listen to AI Audio Walkthrough</span>
            </button>
          </div>
        </div>
      </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Fig 1 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig1_veo_architecture.png" target="_blank">
              <img src="assets/fig1_veo_architecture.png" alt="Figure 1: VEO Pipeline Architecture" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 1: VEO Architecture</p>
            <p class="text-[11px] text-slate-400 leading-tight">Dual-stream metric inversion, connected components failure discovery, and multi-hypothesis classifier.</p>
          </div>

          <!-- Fig 2 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig2_polarity_and_fingerprints.png" target="_blank">
              <img src="assets/fig2_polarity_and_fingerprints.png" alt="Figure 2: Polarity & Fingerprints" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 2: Empirical Fingerprints</p>
            <p class="text-[11px] text-slate-400 leading-tight">Direct vs inverse scale polarity reversal distributions and distinctive per-cause multi-modal radar signatures.</p>
          </div>

          <!-- Fig 3 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig3_intervention_and_downstream.png" target="_blank">
              <img src="assets/fig3_intervention_and_downstream.png" alt="Figure 3: Downstream Boundary Refinement" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 3: Downstream Intervention</p>
            <p class="text-[11px] text-slate-400 leading-tight">Closed-loop boundary-guided bilateral filtering showing regional metric improvement without global distortion.</p>
          </div>
        </div>
      </div>

      <!-- Explainer Video Player & Narrative Storyboard Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Video Player Card (7 Cols) -->
        <div class="lg:col-span-7 bg-slate-900 rounded-2xl border border-slate-800 p-4 shadow-xl space-y-3">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800">
            <div class="flex items-center space-x-2">
              <span class="w-3 h-3 rounded-full bg-red-500"></span>
              <span class="w-3 h-3 rounded-full bg-amber-500"></span>
              <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
              <span class="text-xs font-mono text-slate-400 pl-2">VEO_Executive_Explainer_720p.mp4</span>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">HD 30 FPS</span>
          </div>

          <div class="relative rounded-xl overflow-hidden bg-black aspect-video flex items-center justify-center border border-slate-800 shadow-inner group">
            <video id="explainer-video" class="w-full h-full object-cover" controls poster="assets/fig1_veo_architecture.png">
              <source src="veo_explainer.mp4" type="video/mp4">
              Your browser does not support HTML5 video.
            </video>
          </div>

          <div class="flex items-center justify-between text-xs text-slate-400 pt-1 px-1">
            <span>Explains: The Pain Point → Gaps → Polarity Reversal → VEO 5 Modules</span>
            <button onclick="resetVideo()" class="text-cyan-400 hover:underline">Replay from Beginning</button>
          </div>
        </div>

        <!-- Animated Storyboard Stepper (5 Cols) -->
        <div class="lg:col-span-5 bg-slate-900 rounded-2xl border border-slate-800 p-5 shadow-xl space-y-4">
          <h3 class="text-base font-bold text-white flex items-center space-x-2">
            <i class="fa-solid fa-list-check text-cyan-400"></i>
            <span>Executive Presentation Flow</span>
          </h3>

          <div class="space-y-3">
            <!-- Step 1 -->
            <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-1 hover:border-cyan-500/50 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider">Act 1: The Pain Point</span>
                <span class="text-xs text-slate-500 font-mono">00:00 - 00:07</span>
              </div>
              <h4 class="text-sm font-semibold text-white">The "Flawless Leaderboard" Illusion</h4>
              <p class="text-xs text-slate-300">Depth Anything V2 achieves AbsRel = 0.1040, but global averages conceal catastrophic localized errors where robots misjudge glass and chair legs by meters.</p>
            </div>

            <!-- Step 2 -->
            <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-1 hover:border-red-500/50 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-red-400 uppercase tracking-wider">Act 2: The Critical Gaps</span>
                <span class="text-xs text-slate-500 font-mono">00:07 - 00:15</span>
              </div>
              <h4 class="text-sm font-semibold text-white">Scalar Metrics & Polarity Reversal</h4>
              <p class="text-xs text-slate-300">RMSE only provides 1 number. Furthermore, naive linear regression inverts 3D space (<span class="font-mono text-red-300">s &lt; 0 in 244/244 test scenes</span>), turning geometry inside-out!</p>
            </div>

            <!-- Step 3 -->
            <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-1 hover:border-amber-500/50 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">Act 3: The VEO Paradigm</span>
                <span class="text-xs text-slate-500 font-mono">00:15 - 00:23</span>
              </div>
              <h4 class="text-sm font-semibold text-white">The 5-Module Diagnostic Layer</h4>
              <p class="text-xs text-slate-300">VEO operates post-hoc: M1 (Inverse Alignment s &gt; 0) → M2 (Dense Error Maps) → M3 (Connected Components) → M4 (7 Visual Signals) → M5 (Calibrated Ambiguity Gate).</p>
            </div>

            <!-- Step 4 -->
            <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-1 hover:border-emerald-500/50 transition">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Act 4: Scientific Proofs</span>
                <span class="text-xs text-slate-500 font-mono">00:23 - 00:30</span>
              </div>
              <h4 class="text-sm font-semibold text-white">Human Ground-Truth & Interventions</h4>
              <p class="text-xs text-slate-300">Blinded dual-human agreement reaches κ = 0.472 (58.6% multi-class accuracy). Synthetic texture injection proves explanation faithfulness (0.646 → 0.000 score collapse).</p>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- TAB 2: INTERACTIVE DIAGNOSTIC OBSERVATORY (CORE LAB) -->
    <!-- ========================================================================= -->
    <div id="view-observatory" class="hidden space-y-6">
      
      <!-- Control Bar: Scene Selector & Pipeline HUD -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-wrap items-center justify-between gap-4">
        
        <!-- Scene Dropdown -->
        <div class="flex items-center space-x-3">
          <label class="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Scene:</label>
          <select id="scene-selector" onchange="onSceneChanged()" class="bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-sm font-semibold text-white focus:outline-none focus:border-cyan-500 transition">
            <!-- Dynamically populated -->
          </select>
          <span id="scene-desc" class="text-xs text-slate-400 hidden md:inline"></span>
        </div>

        <!-- Metric Badges -->
        <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
          <div class="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700">
            <span class="text-slate-400">Model:</span> <span class="text-cyan-300 font-bold">Depth Anything V2 (ViT-S)</span>
          </div>
          <div class="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700">
            <span class="text-slate-400">AbsRel:</span> <span id="hud-absrel" class="text-emerald-400 font-bold">-</span>
          </div>
          <div class="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700">
            <span class="text-slate-400">RMSE:</span> <span id="hud-rmse" class="text-emerald-400 font-bold">- m</span>
          </div>
          <div class="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700">
            <span class="text-slate-400">τ85 Error Threshold:</span> <span id="hud-thresh" class="text-amber-400 font-bold">-</span>
          </div>
          <div class="px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700">
            <span class="text-slate-400">Failure Regions:</span> <span id="hud-regions-count" class="text-red-400 font-bold">-</span>
          </div>
        </div>

      </div>

      <!-- 4-View Synchronized Multi-Modal Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <!-- View 1: RGB Image with Bounding Boxes -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-3 space-y-2 shadow-lg">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
              <i class="fa-solid fa-camera text-cyan-400"></i>
              <span>1. Input RGB Image</span>
            </span>
            <span class="text-[10px] text-slate-500 font-mono">640×480 px</span>
          </div>
          <div class="canvas-container rounded-xl overflow-hidden bg-slate-950 aspect-[4/3] border border-slate-800" id="container-rgb">
            <img id="img-rgb" class="w-full h-full object-contain" alt="RGB Input">
            <div id="overlay-boxes" class="absolute inset-0 pointer-events-none"></div>
          </div>
          <p class="text-[11px] text-slate-400">Click any highlighted red box above to inspect its physical failure diagnosis.</p>
        </div>

        <!-- View 2: Model Depth Prediction -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-3 space-y-2 shadow-lg">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
              <i class="fa-solid fa-brain text-purple-400"></i>
              <span>2. Aligned Model Depth</span>
            </span>
            <span class="text-[10px] text-slate-500 font-mono">Inverse OLS (s &gt; 0)</span>
          </div>
          <div class="rounded-xl overflow-hidden bg-slate-950 aspect-[4/3] border border-slate-800">
            <img id="img-pred" class="w-full h-full object-contain" alt="Predicted Depth">
          </div>
          <p class="text-[11px] text-slate-400">Depth Anything V2 aligned via positive scale slope (<span class="font-mono text-cyan-300">s &gt; 0</span> strictly enforced).</p>
        </div>

        <!-- View 3: Ground Truth Depth -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-3 space-y-2 shadow-lg">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
              <i class="fa-solid fa-ruler-combined text-emerald-400"></i>
              <span>3. Ground Truth Depth</span>
            </span>
            <span class="text-[10px] text-slate-500 font-mono">NYU Kinect Sensor</span>
          </div>
          <div class="rounded-xl overflow-hidden bg-slate-950 aspect-[4/3] border border-slate-800">
            <img id="img-gt" class="w-full h-full object-contain" alt="Ground Truth Depth">
          </div>
          <p class="text-[11px] text-slate-400">Dense sensor depth ground truth bounded in [<span class="font-mono">0.7m, 10.0m</span>].</p>
        </div>

        <!-- View 4: Dense Error Heatmap -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-3 space-y-2 shadow-lg">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
              <i class="fa-solid fa-fire text-red-400"></i>
              <span>4. Relative Error Heatmap</span>
            </span>
            <span class="text-[10px] text-slate-500 font-mono">Erel = |D̂ - D| / D</span>
          </div>
          <div class="rounded-xl overflow-hidden bg-slate-950 aspect-[4/3] border border-slate-800">
            <img id="img-error" class="w-full h-full object-contain" alt="Error Heatmap">
          </div>
          <p class="text-[11px] text-slate-400">High relative error clusters isolated at 85th percentile (<span class="font-mono text-red-400">&gt; τ85</span>).</p>
        </div>

      </div>

      <!-- Region Deep-Dive Inspector Panel (Active upon selecting a region) -->
      <div id="region-inspector-card" class="bg-slate-900 border border-cyan-500/40 rounded-2xl p-6 shadow-2xl space-y-6 glow-cyan">
        
        <!-- Inspector Header -->
        <div class="flex flex-wrap items-center justify-between pb-4 border-b border-slate-800 gap-4">
          <div class="flex items-center space-x-3">
            <span id="badge-cause" class="px-3.5 py-1.5 rounded-xl font-bold text-sm bg-cyan-950 text-cyan-300 border border-cyan-800">
              Textureless Surface
            </span>
            <div>
              <h3 id="inspector-title" class="text-lg font-extrabold text-white">Region Deep-Dive Inspector</h3>
              <p id="inspector-subtitle" class="text-xs text-slate-400 font-mono">Bounding Box: [x: 558, y: 57, w: 4, h: 15] | Area: 28 px</p>
            </div>
          </div>

          <!-- Faithfulness Intervention Action -->
          <button onclick="triggerIntervention()" id="btn-intervention" class="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-600 to-red-600 hover:from-amber-500 hover:to-red-500 text-white font-bold text-xs shadow-lg shadow-red-600/20 flex items-center space-x-2 transition">
            <i class="fa-solid fa-wand-magic-sparkles"></i>
            <span>Simulate Physical Intervention: Inject Texture</span>
          </button>
        </div>

        <!-- 3-Column Inspection Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          <!-- Column 1: Feature Signals (4 Cols) -->
          <div class="lg:col-span-4 bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-3">
            <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center justify-between">
              <span>M4: 7 Extracted Evidence Signals</span>
              <i class="fa-solid fa-chart-simple text-cyan-400"></i>
            </h4>

            <div class="space-y-2.5 text-xs">
              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>1. Texture Variance (Var(I)):</span>
                  <span id="feat-var" class="font-mono text-cyan-300 font-bold">176.82</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-var" class="bg-cyan-500 h-1.5 rounded-full" style="width: 35%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>2. Canny Edge Density:</span>
                  <span id="feat-edge" class="font-mono text-slate-200">0.03</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-edge" class="bg-blue-500 h-1.5 rounded-full" style="width: 10%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>3. Luminance Brightness (μ):</span>
                  <span id="feat-bright" class="font-mono text-slate-200">184.2</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-bright" class="bg-amber-500 h-1.5 rounded-full" style="width: 72%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>4. Local Contrast (σ):</span>
                  <span id="feat-contrast" class="font-mono text-slate-200">10.5</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-contrast" class="bg-indigo-500 h-1.5 rounded-full" style="width: 18%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>5. Specular Highlights:</span>
                  <span id="feat-high" class="font-mono text-slate-200">0.00</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-high" class="bg-pink-500 h-1.5 rounded-full" style="width: 0%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>6. Bounding Box AR:</span>
                  <span id="feat-ar" class="font-mono text-slate-200">3.75</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-ar" class="bg-purple-500 h-1.5 rounded-full" style="width: 45%"></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-slate-400 pb-0.5">
                  <span>7. Depth Discontinuity (∇D):</span>
                  <span id="feat-disc" class="font-mono text-slate-200">0.01 m</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div id="bar-disc" class="bg-red-500 h-1.5 rounded-full" style="width: 5%"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Column 2: Mathematical Formula Visualizer & Calibrated Ambiguity Gate (5 Cols) -->
          <div class="lg:col-span-5 bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-4">
            <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center justify-between">
              <span>M5: Formula Execution & Ambiguity Gate</span>
              <i class="fa-solid fa-calculator text-amber-400"></i>
            </h4>

            <!-- Live Formula Substitution -->
            <div class="p-3 rounded-lg bg-slate-900 border border-slate-800 space-y-1.5 font-mono text-xs">
              <span class="text-[10px] text-slate-500 uppercase tracking-wider">Exact Mathematical Attribution:</span>
              <div id="math-formula-box" class="text-cyan-300 text-xs">
                score_textureless = clip(1.0 - 176.82 / 500.0, 0, 1) = <strong class="text-white">0.6464</strong>
              </div>
              <div id="math-sub-formula" class="text-slate-400 text-[11px]">
                Second Leading Hypothesis: score_thin = clip((3.75 - 3.0)/5.0, 0, 1) = 0.1500
              </div>
            </div>

            <!-- Ambiguity Gate Logic Box -->
            <div class="p-3 rounded-lg bg-slate-900/90 border border-slate-800 space-y-2">
              <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider flex items-center space-x-1">
                <i class="fa-solid fa-shield-halved"></i>
                <span>Calibrated Ambiguity Gate Decision Rules:</span>
              </span>
              <div class="grid grid-cols-2 gap-2 text-xs font-mono">
                <div class="p-2 rounded bg-slate-950 border border-slate-800">
                  <div class="text-slate-400 text-[10px]">1. Strong Evidence:</div>
                  <div id="gate-cond1" class="text-emerald-400 font-bold">s(1) = 0.646 ≥ 0.40 (PASS)</div>
                </div>
                <div class="p-2 rounded bg-slate-950 border border-slate-800">
                  <div class="text-slate-400 text-[10px]">2. Margin Delta:</div>
                  <div id="gate-cond2" class="text-emerald-400 font-bold">Δ = 0.496 ≥ 0.10 (PASS)</div>
                </div>
              </div>
              <div id="gate-verdict-text" class="text-xs text-slate-300">
                Gate State: <strong class="text-emerald-400">PASSED</strong> → Confidently assigned to <span class="font-mono text-cyan-300">textureless</span>.
              </div>
            </div>

            <!-- Scores Bar Chart -->
            <div class="h-36 relative">
              <canvas id="chart-scores"></canvas>
            </div>
          </div>

          <!-- Column 3: Prescriptive Engineering Suggestions (3 Cols) -->
          <div class="lg:col-span-3 bg-gradient-to-b from-slate-950 to-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
              <i class="fa-solid fa-lightbulb text-yellow-400"></i>
              <span>Actionable Recommendation</span>
            </h4>
            
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs space-y-2">
              <span class="text-[10px] font-bold text-cyan-400 uppercase">Diagnosis Root Cause:</span>
              <p id="rec-cause" class="text-slate-300 leading-relaxed">
                Texture variance is 176.8 (low). The vision transformer's self-attention lacks high-frequency gradient anchors on flat planar walls and defaults to an ambiguous depth prior.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs space-y-2">
              <span class="text-[10px] font-bold text-emerald-400 uppercase">Model Builder Prescription:</span>
              <p id="rec-prescription" class="text-slate-300 leading-relaxed">
                1. Apply CutBlur / synthetic frequency noise augmentation during fine-tuning.<br>
                2. Enforce normal-guided planar consistency loss (L_normal = 1 - ⟨n, n*⟩) on low-variance regions.
              </p>
            </div>
          </div>

        </div>

      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- TAB 3: SCIENTIFIC VALIDATION & PUBLICATION BENCHMARKS -->
    <!-- ========================================================================= -->
    <div id="view-benchmarks" class="hidden space-y-6">
      
      <!-- Top Title -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-2">
        <h3 class="text-2xl font-extrabold text-white">Scientific Validation & Empirical Benchmark Suite</h3>
        <p class="text-sm text-slate-400">Verified results from 244 held-out scene-disjoint NYU Depth V2 test images and independent multi-rater human audits.</p>
      </div>

      <!-- Grid of Benchmark Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <!-- Card 1: Polarity Reversal Proof -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-xl">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-arrows-spin text-red-400"></i>
              <span>Polarity Reversal Discovery</span>
            </h4>
            <span class="text-[10px] px-2 py-0.5 rounded font-mono bg-red-950 text-red-300 border border-red-800">244/244 Scenes</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Direct depth OLS regression (d = s·p + b) produces negative scale slopes (<strong>s &lt; 0 in 100% of test scenes</strong>), inverting physical geometry. 
            Inverse-depth alignment (1/D ≈ s·P + b) strictly guarantees <strong>s &gt; 0</strong> and optimal metric recovery (AbsRel = 0.1040).
          </p>
          <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs space-y-1">
            <div class="flex justify-between"><span>Direct Depth Fit:</span> <span class="text-red-400 font-bold">s &lt; 0 (Inverted)</span></div>
            <div class="flex justify-between"><span>Inverse Depth (VEO):</span> <span class="text-emerald-400 font-bold">s &gt; 0 (Guaranteed)</span></div>
            <div class="flex justify-between"><span>AbsRel Improvement:</span> <span class="text-cyan-400 font-bold">0.1732 → 0.1040</span></div>
          </div>
        </div>

        <!-- Card 2: Blinded Human Validation -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-xl">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-users text-cyan-400"></i>
              <span>Multi-Rater Human Agreement</span>
            </h4>
            <span class="text-[10px] px-2 py-0.5 rounded font-mono bg-cyan-950 text-cyan-300 border border-cyan-800">N=50 Regions</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Two independent annotators evaluated blinded crops without VEO scores. Inter-rater baseline reached κ = 0.3478. 
            On determinate predictions, VEO achieved <strong>κ = 0.4719 with 58.6% multi-class accuracy</strong>.
          </p>
          <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs space-y-1">
            <div class="flex justify-between"><span>Human Inter-Rater:</span> <span class="text-slate-300">κ = 0.3478 (46.0%)</span></div>
            <div class="flex justify-between"><span>VEO vs Human Raters:</span> <span class="text-cyan-400 font-bold">κ = 0.4719 (58.6%)</span></div>
            <div class="flex justify-between"><span>Textureless Precision:</span> <span class="text-emerald-400 font-bold">87.5% Precision</span></div>
          </div>
        </div>

        <!-- Card 3: Downstream Model Refinement -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4 shadow-xl">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-white flex items-center space-x-2">
              <i class="fa-solid fa-wrench text-emerald-400"></i>
              <span>Boundary Bilateral Refinement</span>
            </h4>
            <span class="text-[10px] px-2 py-0.5 rounded font-mono bg-emerald-950 text-emerald-300 border border-emerald-800">207 Test Scenes</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            VEO-guided localized edge-preserving bilateral smoothing inside boundary mixing masks reduced regional boundary RMSE and AbsRel without global distortion.
          </p>
          <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs space-y-1">
            <div class="flex justify-between"><span>Regional RMSE:</span> <span class="text-emerald-400 font-bold">0.6629 → 0.6618 m</span></div>
            <div class="flex justify-between"><span>Regional AbsRel:</span> <span class="text-emerald-400 font-bold">0.2348 → 0.2340</span></div>
            <div class="flex justify-between"><span>Global Full-Scene RMSE:</span> <span class="text-cyan-400 font-bold">0.4658 m (0.00% distortion)</span></div>
          </div>
        </div>

      </div>

      <!-- Feature-Error Correlation Table -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <h4 class="text-base font-bold text-white flex items-center space-x-2">
          <i class="fa-solid fa-table text-cyan-400"></i>
          <span>Feature-Error Statistical Correlation Matrix (N = 5,236 Failure Regions)</span>
        </h4>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs font-mono">
            <thead class="bg-slate-800/80 text-slate-300 uppercase">
              <tr>
                <th class="p-3">Feature Evidence Signal</th>
                <th class="p-3">Pearson Correlation (r)</th>
                <th class="p-3">p-value</th>
                <th class="p-3">Physical Mechanism Explained</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 text-slate-300">
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white">depth_discontinuity</td>
                <td class="p-3 text-cyan-400 font-bold">0.4502</td>
                <td class="p-3">9.36 × 10⁻²⁶⁰</td>
                <td class="p-3">Sharp object depth boundaries trigger severe foreground/background bleeding.</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white">contrast</td>
                <td class="p-3 text-cyan-400 font-bold">0.2656</td>
                <td class="p-3">2.98 × 10⁻⁸⁵</td>
                <td class="p-3">Low local contrast depresses feature activations and confidence.</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white">texture_var</td>
                <td class="p-3 text-cyan-400 font-bold">0.2165</td>
                <td class="p-3">1.47 × 10⁻⁵⁶</td>
                <td class="p-3">Lack of texture on flat walls causes self-attention map diffusion.</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white">brightness</td>
                <td class="p-3 text-cyan-400 font-bold">0.1643</td>
                <td class="p-3">5.07 × 10⁻³³</td>
                <td class="p-3">Under-exposed shadows and over-exposed highlight glares.</td>
              </tr>
              <tr class="hover:bg-slate-800/40">
                <td class="p-3 font-bold text-white">highlight_ratio</td>
                <td class="p-3 text-cyan-400 font-bold">0.1398</td>
                <td class="p-3">2.88 × 10⁻²⁴</td>
                <td class="p-3">Non-Lambertian specular reflections violate diffuse surface priors.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- High-Resolution Publication Figure Gallery -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
        <div class="flex items-center justify-between">
          <h4 class="text-base font-bold text-white flex items-center space-x-2">
            <i class="fa-solid fa-cube text-cyan-400"></i>
            <span>Publication Diagrams & Empirical Figures</span>
          </h4>
          <span class="text-xs text-slate-400">Click any figure to expand</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Fig 1 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig1_veo_architecture.png" target="_blank">
              <img src="assets/fig1_veo_architecture.png" alt="Figure 1: VEO Pipeline Architecture" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 1: VEO Architecture</p>
            <p class="text-[11px] text-slate-400 leading-tight">Dual-stream metric inversion, connected components failure discovery, and multi-hypothesis classifier.</p>
          </div>

          <!-- Fig 2 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig2_polarity_and_fingerprints.png" target="_blank">
              <img src="assets/fig2_polarity_and_fingerprints.png" alt="Figure 2: Polarity & Fingerprints" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 2: Empirical Fingerprints</p>
            <p class="text-[11px] text-slate-400 leading-tight">Direct vs inverse scale polarity reversal distributions and distinctive per-cause multi-modal radar signatures.</p>
          </div>

          <!-- Fig 3 -->
          <div class="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden p-3 space-y-2 hover:border-cyan-500/50 transition">
            <a href="assets/fig3_intervention_and_downstream.png" target="_blank">
              <img src="assets/fig3_intervention_and_downstream.png" alt="Figure 3: Downstream Boundary Refinement" class="rounded-lg w-full h-44 object-cover object-top border border-slate-800 hover:opacity-90 transition">
            </a>
            <p class="text-xs font-bold text-slate-200">Figure 3: Downstream Intervention</p>
            <p class="text-[11px] text-slate-400 leading-tight">Closed-loop boundary-guided bilateral filtering showing regional metric improvement without global distortion.</p>
          </div>
        </div>
      </div>

    </div>

  </main>

  <!-- Embedded VEO Application Data (Guarantees zero-CORS offline execution) -->
  <script>
    window.VEO_DATA = {data_json_str};
  </script>

  <!-- Application Logic Script -->
  <script>
    let currentScene = null;
    let selectedRegion = null;
    let scoresChart = null;
    let isIntervened = false;

    function initApp() {{
      const scenes = window.VEO_DATA.scenes;
      const selector = document.getElementById('scene-selector');
      selector.innerHTML = '';

      scenes.forEach(s => {{
        const opt = document.createElement('option');
        opt.value = s.sample_id;
        opt.textContent = `${{s.sample_id.toUpperCase()}} (${{s.regions.length}} regions)`;
        selector.appendChild(opt);
      }});

      if (scenes.length > 0) {{
        loadScene(scenes[0].sample_id);
      }}
    }}

    function switchTab(tabId) {{
      ['explainer', 'observatory', 'benchmarks'].forEach(t => {{
        document.getElementById(`view-${{t}}`).classList.add('hidden');
        document.getElementById(`tab-${{t}}`).classList.remove('active');
        document.getElementById(`tab-${{t}}`).classList.add('text-slate-400');
      }});

      document.getElementById(`view-${{tabId}}`).classList.remove('hidden');
      document.getElementById(`tab-${{tabId}}`).classList.add('active');
      document.getElementById(`tab-${{tabId}}`).classList.remove('text-slate-400');

      if (tabId === 'observatory' && !selectedRegion && currentScene && currentScene.regions.length > 0) {{
        // Select first region
        selectRegion(currentScene.regions[0].region_id);
      }}
    }}

    function onSceneChanged() {{
      const sid = document.getElementById('scene-selector').value;
      loadScene(sid);
    }}

    function loadScene(sampleId) {{
      currentScene = window.VEO_DATA.scenes.find(s => s.sample_id === sampleId);
      if (!currentScene) return;

      isIntervened = false;

      // Update HUD
      document.getElementById('scene-desc').textContent = currentScene.description;
      document.getElementById('hud-absrel').textContent = currentScene.metrics.abs_rel.toFixed(4);
      document.getElementById('hud-rmse').textContent = currentScene.metrics.rmse.toFixed(4) + ' m';
      document.getElementById('hud-thresh').textContent = currentScene.metrics.threshold.toFixed(4);
      document.getElementById('hud-regions-count').textContent = currentScene.regions.length + ' Clusters';

      // Update Images
      document.getElementById('img-rgb').src = currentScene.images.rgb;
      document.getElementById('img-pred').src = currentScene.images.depth_pred;
      document.getElementById('img-gt').src = currentScene.images.depth_gt;
      document.getElementById('img-error').src = currentScene.images.error_map;

      // Render Bounding Boxes on RGB image
      renderBoundingBoxes();

      // Automatically select first clear failure region
      if (currentScene.regions.length > 0) {{
        selectRegion(currentScene.regions[0].region_id);
      }}
    }}

    function renderBoundingBoxes() {{
      const overlay = document.getElementById('overlay-boxes');
      overlay.innerHTML = '';

      const img = document.getElementById('img-rgb');
      const imgW = 640;
      const imgH = 480;

      currentScene.regions.forEach((reg, idx) => {{
        const [x, y, w, h] = reg.bbox;

        const leftPct = (x / imgW) * 100;
        const topPct = (y / imgH) * 100;
        const widthPct = (w / imgW) * 100;
        const heightPct = (h / imgH) * 100;

        const box = document.createElement('div');
        box.className = 'bbox-highlight';
        box.id = `box-reg-${{reg.region_id}}`;
        box.style.left = `${{leftPct}}%`;
        box.style.top = `${{topPct}}%`;
        box.style.width = `${{Math.max(widthPct, 2)}}%`;
        box.style.height = `${{Math.max(heightPct, 2)}}%`;
        box.title = `Region ${{reg.region_id}}: ${{reg.top_cause}} (Error: ${{(reg.mean_error * 100).toFixed(1)}}%)`;

        box.onclick = (e) => {{
          e.stopPropagation();
          selectRegion(reg.region_id);
        }};

        overlay.appendChild(box);
      }});
    }}

    function selectRegion(regionId) {{
      if (!currentScene) return;
      selectedRegion = currentScene.regions.find(r => r.region_id === regionId);
      if (!selectedRegion) return;

      isIntervened = false;
      document.getElementById('btn-intervention').innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i><span>Simulate Physical Intervention: Inject Texture</span>`;
      document.getElementById('btn-intervention').classList.remove('from-emerald-600', 'to-teal-600');
      document.getElementById('btn-intervention').classList.add('from-amber-600', 'to-red-600');

      // Highlight active box
      document.querySelectorAll('.bbox-highlight').forEach(el => el.classList.remove('selected'));
      const activeBox = document.getElementById(`box-reg-${{regionId}}`);
      if (activeBox) activeBox.classList.add('selected');

      updateInspectorUI(selectedRegion);
    }}

    function updateInspectorUI(reg, customFeatures = null, customScores = null, customTopCause = null) {{
      const feats = customFeatures || reg.features;
      const scores = customScores || reg.scores;
      const cause = customTopCause || reg.top_cause;

      // Badges & Titles
      const badge = document.getElementById('badge-cause');
      badge.textContent = formatCategoryName(cause);
      badge.className = `px-3.5 py-1.5 rounded-xl font-bold text-sm ${{getCategoryBadgeClass(cause)}}`;

      document.getElementById('inspector-title').textContent = `Region ${{reg.region_id}}: ${{formatCategoryName(cause)}}`;
      document.getElementById('inspector-subtitle').textContent = 
        `Bounding Box: [x: ${{reg.bbox[0]}}, y: ${{reg.bbox[1]}}, w: ${{reg.bbox[2]}}, h: ${{reg.bbox[3]}}] | Area: ${{reg.area}} px | Mean Error: ${{(reg.mean_error * 100).toFixed(1)}}%`;

      // 7 Evidence Signals
      document.getElementById('feat-var').textContent = feats.texture_var.toFixed(2);
      document.getElementById('bar-var').style.width = `${{Math.min((feats.texture_var / 500) * 100, 100)}}%`;

      document.getElementById('feat-edge').textContent = feats.edge_density.toFixed(3);
      document.getElementById('bar-edge').style.width = `${{Math.min(feats.edge_density * 300, 100)}}%`;

      document.getElementById('feat-bright').textContent = feats.brightness.toFixed(1);
      document.getElementById('bar-bright').style.width = `${{(feats.brightness / 255) * 100}}%`;

      document.getElementById('feat-contrast').textContent = feats.contrast.toFixed(1);
      document.getElementById('bar-contrast').style.width = `${{Math.min((feats.contrast / 60) * 100, 100)}}%`;

      document.getElementById('feat-high').textContent = (feats.highlight_ratio * 100).toFixed(1) + '%';
      document.getElementById('bar-high').style.width = `${{Math.min(feats.highlight_ratio * 100, 100)}}%`;

      document.getElementById('feat-ar').textContent = feats.aspect_ratio.toFixed(2);
      document.getElementById('bar-ar').style.width = `${{Math.min((feats.aspect_ratio / 8) * 100, 100)}}%`;

      document.getElementById('feat-disc').textContent = feats.depth_discontinuity.toFixed(3) + ' m';
      document.getElementById('bar-disc').style.width = `${{Math.min(feats.depth_discontinuity * 100, 100)}}%`;

      // Live Mathematical Formula Box
      const topScoreVal = scores[cause] || Math.max(...Object.values(scores));
      if (cause === 'textureless') {{
        document.getElementById('math-formula-box').innerHTML = 
          `score_textureless = clip(1.0 - ${{feats.texture_var.toFixed(2)}} / 500.0, 0, 1) = <strong class="text-white">${{topScoreVal.toFixed(4)}}</strong>`;
      }} else if (cause === 'boundary_mixing') {{
        document.getElementById('math-formula-box').innerHTML = 
          `score_boundary = clip(${{feats.edge_density.toFixed(3)}} × 3.0, 0, 1) = <strong class="text-white">${{topScoreVal.toFixed(4)}}</strong>`;
      }} else if (cause === 'reflection') {{
        document.getElementById('math-formula-box').innerHTML = 
          `score_reflection = clip(${{feats.highlight_ratio.toFixed(3)}} × 5.0, 0, 1) = <strong class="text-white">${{topScoreVal.toFixed(4)}}</strong>`;
      }} else if (cause === 'thin_object') {{
        document.getElementById('math-formula-box').innerHTML = 
          `score_thin = clip((${{feats.aspect_ratio.toFixed(2)}} - 3.0) / 5.0, 0, 1) = <strong class="text-white">${{topScoreVal.toFixed(4)}}</strong>`;
      }} else {{
        document.getElementById('math-formula-box').innerHTML = 
          `Top Score Formula: <strong class="text-white">${{topScoreVal.toFixed(4)}}</strong> (Ambiguity Margin &lt; 0.10)`;
      }}

      // Ambiguity Gate
      const sortedScores = Object.entries(scores).sort((a,b) => b[1] - a[1]);
      const s1 = sortedScores[0][1];
      const s2 = sortedScores.length > 1 ? sortedScores[1][1] : 0;
      const margin = s1 - s2;

      const cond1Pass = s1 >= 0.40;
      const cond2Pass = margin >= 0.10;

      document.getElementById('gate-cond1').innerHTML = `s(1) = ${{s1.toFixed(3)}} ${{cond1Pass ? '≥ 0.40 (PASS)' : '&lt; 0.40 (FAIL)'}}`;
      document.getElementById('gate-cond1').className = cond1Pass ? "text-emerald-400 font-bold" : "text-red-400 font-bold";

      document.getElementById('gate-cond2').innerHTML = `Δ = ${{margin.toFixed(3)}} ${{cond2Pass ? '≥ 0.10 (PASS)' : '&lt; 0.10 (FAIL)'}}`;
      document.getElementById('gate-cond2').className = cond2Pass ? "text-emerald-400 font-bold" : "text-red-400 font-bold";

      if (cond1Pass && cond2Pass) {{
        document.getElementById('gate-verdict-text').innerHTML = 
          `Gate State: <strong class="text-emerald-400">PASSED</strong> → Confidently categorized as <span class="font-mono text-cyan-300 font-bold">${{formatCategoryName(sortedScores[0][0])}}</span>.`;
      }} else {{
        document.getElementById('gate-verdict-text').innerHTML = 
          `Gate State: <strong class="text-amber-400">AMBIGUOUS</strong> → Competing hypotheses or weak evidence. Ambiguity gate triggered to prevent false certainty!`;
      }}

      // Prescriptions
      updatePrescriptions(cause, feats);

      // Render Scores Chart
      renderScoresChart(scores);
    }}

    function updatePrescriptions(cause, feats) {{
      const causeBox = document.getElementById('rec-cause');
      const prescBox = document.getElementById('rec-prescription');

      if (cause === 'textureless') {{
        causeBox.innerHTML = `Texture variance is extremely low (${{feats.texture_var.toFixed(1)}} vs threshold 500). Transformers lack gradient key-value tokens on planar walls and predict flat unanchored depth.`;
        prescBox.innerHTML = `1. Inject CutBlur / synthetic frequency noise augmentation during model fine-tuning.<br>2. Enforce surface normal planar consistency loss (L_normal = 1 - ⟨n, n*⟩) across low-variance masks.`;
      }} else if (cause === 'boundary_mixing') {{
        causeBox.innerHTML = `High edge density (${{feats.edge_density.toFixed(2)}}) with boundary depth discontinuity (${{feats.depth_discontinuity.toFixed(2)}}m). The model bleeds foreground depth into background.`;
        prescBox.innerHTML = `1. Add edge-aware depth smoothness loss (L_edge = |∇d| · exp(-|∇I|)).<br>2. Apply VEO-guided bilateral boundary refinement (+0.35% AbsRel gain verified in paper Table IX).`;
      }} else if (cause === 'reflection') {{
        causeBox.innerHTML = `High specular highlight ratio (${{(feats.highlight_ratio*100).toFixed(1)}}%). Non-Lambertian glossy floor reflections violate diffuse photometric assumptions.`;
        prescBox.innerHTML = `1. Apply HSV specular attenuation masking in self-supervised photometric losses.<br>2. Add multi-view polarization or reflection-invariant augmentations.`;
      }} else if (cause === 'thin_object') {{
        causeBox.innerHTML = `Elongated aspect ratio (${{feats.aspect_ratio.toFixed(1)}} &gt; 3.0). Slender chair legs and cords are blurred away by patch tokenization.`;
        prescBox.innerHTML = `1. Use high-resolution multi-scale feature pyramids (e.g. Swin / DPT multi-scale tokens).<br>2. Incorporate boundary gradient matching loss on thin structures.`;
      }} else {{
        causeBox.innerHTML = `Multi-signal ambiguity. Competing hypotheses or low overall feature response in complex indoor geometry.`;
        prescBox.innerHTML = `1. Conservative ambiguity flagging prevents false certainty in safety-critical robotics.<br>2. Use multi-frame temporal consensus filtering to resolve ambiguity.`;
      }}
    }}

    function renderScoresChart(scores) {{
      const ctx = document.getElementById('chart-scores').getContext('2d');
      const labels = ['Textureless', 'Boundary', 'Reflection', 'Thin Object', 'Lighting', 'Occlusion'];
      const dataVals = [
        scores.textureless || 0,
        scores.boundary_mixing || 0,
        scores.reflection || 0,
        scores.thin_object || 0,
        scores.poor_lighting || 0,
        scores.occlusion || 0
      ];

      if (scoresChart) {{
        scoresChart.destroy();
      }}

      scoresChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: labels,
          datasets: [{{
            label: 'Hypothesis Score [0, 1]',
            data: dataVals,
            backgroundColor: [
              '#38BDF8', '#3B82F6', '#EC4899', '#A855F7', '#F59E0B', '#EF4444'
            ],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{ enabled: true }}
          }},
          scales: {{
            x: {{
              min: 0,
              max: 1.0,
              grid: {{ color: '#1E293B' }},
              ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}
            }},
            y: {{
              grid: {{ display: false }},
              ticks: {{ color: '#E2E8F0', font: {{ size: 10 }} }}
            }}
          }}
        }}
      }});
    }}

    function triggerIntervention() {{
      if (!selectedRegion) return;

      if (!isIntervened) {{
        // Apply synthetic texture intervention
        isIntervened = true;
        const newFeats = {{ ...selectedRegion.features, texture_var: 689.39 }};
        const newScores = {{
          ...selectedRegion.scores,
          textureless: 0.0,
          boundary_mixing: 0.093
        }};
        
        updateInspectorUI(selectedRegion, newFeats, newScores, 'ambiguous');

        document.getElementById('btn-intervention').innerHTML = 
          `<i class="fa-solid fa-rotate-left"></i><span>Reset to Original State (Revert Texture)</span>`;
        document.getElementById('btn-intervention').classList.remove('from-amber-600', 'to-red-600');
        document.getElementById('btn-intervention').classList.add('from-emerald-600', 'to-teal-600');
      }} else {{
        // Reset
        isIntervened = false;
        updateInspectorUI(selectedRegion);
        document.getElementById('btn-intervention').innerHTML = 
          `<i class="fa-solid fa-wand-magic-sparkles"></i><span>Simulate Physical Intervention: Inject Texture</span>`;
        document.getElementById('btn-intervention').classList.remove('from-emerald-600', 'to-teal-600');
        document.getElementById('btn-intervention').classList.add('from-amber-600', 'to-red-600');
      }}
    }}

    function playExplainerVoiceover() {{
      if (!('speechSynthesis' in window)) {{
        alert("Speech synthesis is not supported in this browser.");
        return;
      }}

      window.speechSynthesis.cancel();
      const narrationText = 
        "Welcome to the Vision Error Observatory, or VEO. " +
        "Modern depth estimation models achieve impressive benchmark scores on paper, but global averages hide severe localized errors. " +
        "In real indoor scenes, glass reflections, flat textureless walls, and thin chair legs cause localized 3-meter depth errors that can crash autonomous robots. " +
        "VEO solves this observability gap. By isolating high-error regions with connected components, extracting seven physical evidence signals, " +
        "and applying a calibrated ambiguity gate, VEO explains where and why depth models fail, and guides engineers to fix them.";

      const utterance = new SpeechSynthesisUtterance(narrationText);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;

      const btn = document.getElementById('btn-voiceover');
      btn.innerHTML = `<i class="fa-solid fa-circle-stop text-red-400"></i><span>Stop AI Audio</span>`;
      btn.onclick = () => {{
        window.speechSynthesis.cancel();
        btn.innerHTML = `<i class="fa-solid fa-volume-high text-cyan-400"></i><span>Listen to AI Audio Walkthrough</span>`;
        btn.onclick = playExplainerVoiceover;
      }};

      utterance.onend = () => {{
        btn.innerHTML = `<i class="fa-solid fa-volume-high text-cyan-400"></i><span>Listen to AI Audio Walkthrough</span>`;
        btn.onclick = playExplainerVoiceover;
      }};

      window.speechSynthesis.speak(utterance);
    }}

    function resetVideo() {{
      const video = document.getElementById('explainer-video');
      video.currentTime = 0;
      video.play();
    }}

    function formatCategoryName(cat) {{
      const map = {{
        'textureless': 'Textureless Surface',
        'boundary_mixing': 'Boundary Mixing / Bleed',
        'reflection': 'Specular Reflection',
        'thin_object': 'Thin Slender Structure',
        'poor_lighting': 'Poor / Extreme Lighting',
        'occlusion': 'Occlusion Discontinuity',
        'ambiguous': 'Ambiguous / Multi-Cause'
      }};
      return map[cat] || cat;
    }}

    function getCategoryBadgeClass(cat) {{
      const map = {{
        'textureless': 'bg-cyan-950 text-cyan-300 border border-cyan-800',
        'boundary_mixing': 'bg-blue-950 text-blue-300 border border-blue-800',
        'reflection': 'bg-pink-950 text-pink-300 border border-pink-800',
        'thin_object': 'bg-purple-950 text-purple-300 border border-purple-800',
        'poor_lighting': 'bg-amber-950 text-amber-300 border border-amber-800',
        'occlusion': 'bg-red-950 text-red-300 border border-red-800',
        'ambiguous': 'bg-slate-800 text-slate-300 border border-slate-700'
      }};
      return map[cat] || 'bg-slate-800 text-slate-300 border border-slate-700';
    }}

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', initApp);
  </script>

</body>
</html>
"""

    out_file = Path("web_app/index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[OK] Interactive Web Application successfully generated at:")
    print(f"     {out_file.resolve()} (Size: {out_file.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_web_app_html()
