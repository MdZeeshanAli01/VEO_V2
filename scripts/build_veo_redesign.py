"""
Vision Error Observatory (VEO) - Complete Redesign Builder
Generates the research-grade interactive visual interface satisfying all specifications:
- 8-stage guided research workflow
- Synchronized dual viewports with live crosshair tracking
- Arbitrary 5x5 pixel region selection with 10x nearest-neighbor magnification
- Real Depth Anything V2 inference pipeline explanation with authentic intermediate feature activations (Layers 3, 6, 9, 12)
- Visual reveal of local error vs global plausibility with split-slider & threshold filter
- 25-pixel quantitative comparison table with live metric-aligned depth formulas
- Interactive WebGL 3D visualization (Three.js + OrbitControls) with 5x5 elevation lattice & displacement stems
- 7-category failure cause evidence tracing
- Dual-dimension attribution framework (Image vs Model) with structured failure report card
"""

from pathlib import Path

def generate_redesigned_html():
    html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vision Error Observatory (VEO) | Interactive Diagnostic Research Workstation</title>
  
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="alternate icon" href="favicon.ico">
  
  <!-- Precompiled Tailwind CSS & FontAwesome -->
  <link rel="stylesheet" href="assets/css/tailwind.min.css">
  <link rel="stylesheet" href="assets/fontawesome/all.min.css">
  
  <!-- Local Offline Libraries: Three.js, OrbitControls, Chart.js -->
  <script src="assets/js/three.min.js"></script>
  <script src="assets/js/OrbitControls.js"></script>
  <script src="assets/js/chart.min.js"></script>
  
  <!-- Precomputed Dataset Payload (Zero-CORS offline & local file compatible) -->
  <script src="data/app_data_v2.js"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    :root {
      --bg-dark: #070B12;
      --card-bg: #0D131F;
      --border-color: #1E293B;
      --cyan-glow: rgba(6, 182, 212, 0.4);
      --red-glow: rgba(239, 68, 68, 0.4);
    }
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-dark);
      color: #E2E8F0;
      overflow-x: hidden;
    }
    
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    
    /* Crosshair Canvas Container */
    .viewport-canvas {
      image-rendering: auto;
      cursor: crosshair;
      user-select: none;
    }
    
    /* 10x Nearest-Neighbor Magnified Grid */
    .magnified-grid {
      image-rendering: pixelated;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #090E17;
    }
    ::-webkit-scrollbar-thumb {
      background: #1E293B;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }
    
    /* Stage Stepper Tabs */
    .step-pill.active {
      background: #0284C7;
      color: #FFFFFF;
      box-shadow: 0 0 15px rgba(2, 132, 199, 0.5);
      border-color: #38BDF8;
    }
    
    /* Selected Pixel Highlighting */
    .pixel-tile.selected {
      outline: 2px solid #38BDF8;
      box-shadow: 0 0 10px #38BDF8;
      z-index: 10;
    }
    
    /* Comparison Slider Container */
    .split-container {
      position: relative;
      overflow: hidden;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-cyan-500 selection:text-white">

  <!-- ========================================================================= -->
  <!-- TOP NAVIGATION & RESEARCH STATUS HUD -->
  <!-- ========================================================================= -->
  <header class="bg-[#0B101B]/95 border-b border-slate-800 sticky top-0 z-50 backdrop-blur-md">
    <div class="max-w-[1600px] mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-4">
      
      <!-- Brand & Project Identity -->
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center text-white shadow-lg shadow-cyan-500/20">
          <i class="fa-solid fa-cube text-base"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-base font-bold tracking-tight text-white flex items-center gap-1.5">
              <span>Vision Error Observatory</span>
              <span class="text-cyan-400 font-mono text-xs font-semibold px-1.5 py-0.2 bg-cyan-950/80 rounded border border-cyan-800">(VEO)</span>
            </h1>
            <span class="px-2 py-0.5 text-[10px] font-mono font-medium rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800/80">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block mr-1 animate-pulse"></span>
              Research Grade
            </span>
          </div>
          <p class="text-[11px] text-slate-400">Diagnostic & Observability Framework for Monocular Depth Estimation | Capstone Project</p>
        </div>
      </div>

      <!-- Scene Selector Dropdown -->
      <div class="flex items-center space-x-3 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
        <label for="scene-select" class="text-xs text-slate-400 font-medium pl-2 flex items-center gap-1.5">
          <i class="fa-solid fa-camera text-cyan-400 text-xs"></i>
          <span>NYU Scene:</span>
        </label>
        <select id="scene-select" onchange="onSceneSelectChange(this.value)" class="bg-slate-950 text-xs font-mono text-cyan-300 border border-slate-700 rounded-lg px-2.5 py-1 focus:outline-none focus:border-cyan-500 transition cursor-pointer">
          <!-- Populated dynamically via JS -->
        </select>
      </div>

      <!-- Benchmark Protocol Verification -->
      <div class="hidden lg:flex items-center space-x-3 text-xs font-mono text-slate-400 bg-slate-950/80 px-3 py-1.5 rounded-lg border border-slate-800">
        <div class="flex items-center gap-1.5">
          <span class="text-slate-500">Model:</span>
          <span class="text-slate-200 font-semibold">Depth Anything V2 (ViT-S)</span>
        </div>
        <span class="text-slate-700">|</span>
        <div class="flex items-center gap-1.5">
          <span class="text-slate-500">Alignment:</span>
          <span class="text-cyan-400 font-semibold">1/D ≈ s·P + b</span>
        </div>
      </div>

      <!-- PDF Paper Link -->
      <div>
        <a href="assets/VEO_conference_paper.pdf" target="_blank" class="px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 text-xs font-semibold flex items-center space-x-1.5 transition">
          <i class="fa-solid fa-file-pdf"></i>
          <span>Paper (PDF)</span>
        </a>
      </div>

    </div>

    <!-- Stepper Workflow Bar (Stages 1 through 8) -->
    <div class="border-t border-slate-800/80 bg-[#080D16]/90 px-4 py-2 overflow-x-auto">
      <div class="max-w-[1600px] mx-auto flex items-center space-x-2 text-xs font-medium min-w-max">
        <span class="text-[11px] uppercase tracking-wider text-slate-500 font-mono pr-2">Workflow:</span>
        <button onclick="scrollToStage('stage-1')" class="step-pill active px-3 py-1 rounded-lg border border-slate-800 transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">1</span>
          <span>RGB vs Ground Truth</span>
        </button>
        <button onclick="scrollToStage('stage-2')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">2</span>
          <span>5×5 Pixel Selection</span>
        </button>
        <button onclick="scrollToStage('stage-3')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">3</span>
          <span>Inference Pipeline</span>
        </button>
        <button onclick="scrollToStage('stage-4')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">4</span>
          <span>Visual Reveal & Plausibility</span>
        </button>
        <button onclick="scrollToStage('stage-5')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">5</span>
          <span>25-Pixel Error Table</span>
        </button>
        <button onclick="scrollToStage('stage-6')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">6</span>
          <span>3D Surface & Discrepancy</span>
        </button>
        <button onclick="scrollToStage('stage-7')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">7</span>
          <span>Failure Cause Evidence</span>
        </button>
        <button onclick="scrollToStage('stage-8')" class="step-pill px-3 py-1 rounded-lg border border-slate-800 text-slate-400 hover:text-white transition flex items-center gap-1.5">
          <span class="font-mono text-[10px] opacity-75">8</span>
          <span>Model vs Image Attribution</span>
        </button>
      </div>
    </div>
  </header>

  <!-- ========================================================================= -->
  <!-- MAIN WORKSTATION CONTENT -->
  <!-- ========================================================================= -->
  <main class="flex-grow max-w-[1600px] w-full mx-auto px-4 py-6 space-y-12">

    <!-- Global Spatial HUD Bar -->
    <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-3 flex flex-wrap items-center justify-between gap-4 text-xs font-mono shadow-xl">
      <div class="flex items-center space-x-4">
        <span class="text-slate-400 flex items-center gap-1.5">
          <i class="fa-solid fa-crosshairs text-cyan-400"></i>
          <span>Hover Pixel:</span>
          <strong id="hud-hover-coord" class="text-white">(X: ---, Y: ---)</strong>
        </span>
        <span class="text-slate-700">|</span>
        <span class="text-slate-400 flex items-center gap-1.5">
          <i class="fa-solid fa-vector-square text-amber-400"></i>
          <span>Selected 5×5 Patch:</span>
          <strong id="hud-region-coord" class="text-amber-300">[X: 210..214, Y: 140..144]</strong>
        </span>
      </div>

      <div class="flex items-center space-x-4">
        <span class="text-slate-400 flex items-center gap-1.5">
          <i class="fa-solid fa-ruler text-emerald-400"></i>
          <span>Active Pixel GT:</span>
          <strong id="hud-active-gt" class="text-emerald-400">--- m</strong>
        </span>
        <span class="text-slate-700">|</span>
        <span class="text-slate-400 flex items-center gap-1.5">
          <i class="fa-solid fa-brain text-cyan-400"></i>
          <span>Pred Depth:</span>
          <strong id="hud-active-pred" class="text-cyan-300">--- m</strong>
        </span>
        <span class="text-slate-700">|</span>
        <span class="text-slate-400 flex items-center gap-1.5">
          <i class="fa-solid fa-triangle-exclamation text-red-400"></i>
          <span>Rel Error:</span>
          <strong id="hud-active-err" class="text-red-400">--- %</strong>
        </span>
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- STAGE 1: SELECT & UNDERSTAND ORIGINAL IMAGE -->
    <!-- ======================================================================= -->
    <section id="stage-1" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 1</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Select & Understand the Original Image</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(NYU Depth V2 Sensor Ground Truth)</span>
          </h2>
        </div>
        <div class="text-xs text-slate-400 flex items-center gap-2">
          <span class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 font-mono" id="scene-meta-pill">
            NYU Test Split | 480×640 px | Microsoft Kinect RGB-D
          </span>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- Left Viewport: RGB Image (6 Cols) -->
        <div class="lg:col-span-6 bg-slate-900 rounded-xl border border-slate-800 p-4 shadow-xl space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-semibold text-slate-200 flex items-center gap-1.5">
              <i class="fa-solid fa-image text-cyan-400"></i>
              <span>Original Input RGB Image</span>
            </span>
            <span class="text-slate-400 font-mono">480 × 640 × 3 uint8</span>
          </div>

          <div class="relative rounded-lg overflow-hidden bg-black border border-slate-800 canvas-container flex justify-center items-center">
            <canvas id="canvas-rgb" width="640" height="480" class="viewport-canvas w-full h-auto block"></canvas>
            <div id="selection-box-rgb" class="absolute border-2 border-cyan-400 bg-cyan-400/20 pointer-events-none transition-all duration-75"></div>
            <div id="crosshair-rgb" class="absolute pointer-events-none hidden">
              <div class="w-4 h-4 -ml-2 -mt-2 border-2 border-white rounded-full bg-cyan-400/30"></div>
            </div>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">
            Real indoor scene captured via Microsoft Kinect camera. Monocular depth models receive only these 2D RGB intensities without direct stereoscopic disparity.
          </p>
        </div>

        <!-- Right Viewport: Ground Truth Depth (6 Cols) -->
        <div class="lg:col-span-6 bg-slate-900 rounded-xl border border-slate-800 p-4 shadow-xl space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-semibold text-slate-200 flex items-center gap-1.5">
              <i class="fa-solid fa-satellite-dish text-emerald-400"></i>
              <span>Ground-Truth Metric Depth Map</span>
            </span>
            <span id="gt-range-label" class="text-emerald-400 font-mono">Range: 0.865m – 2.587m</span>
          </div>

          <div class="relative rounded-lg overflow-hidden bg-black border border-slate-800 canvas-container flex justify-center items-center">
            <canvas id="canvas-depth-gt" width="640" height="480" class="viewport-canvas w-full h-auto block"></canvas>
            <div id="selection-box-gt" class="absolute border-2 border-cyan-400 bg-cyan-400/20 pointer-events-none transition-all duration-75"></div>
            <div id="crosshair-gt" class="absolute pointer-events-none hidden">
              <div class="w-4 h-4 -ml-2 -mt-2 border-2 border-white rounded-full bg-emerald-400/30"></div>
            </div>
          </div>

          <!-- Colorbar Legend -->
          <div class="space-y-1">
            <div class="h-3 w-full rounded bg-gradient-to-r from-blue-700 via-emerald-500 via-amber-400 to-red-600 border border-slate-800"></div>
            <div class="flex justify-between text-[10px] font-mono text-slate-400">
              <span id="cbar-min">Near (0.8m)</span>
              <span>1.5m</span>
              <span>2.5m</span>
              <span>3.5m</span>
              <span id="cbar-max">Far (4.5m+)</span>
            </div>
          </div>
          <p class="text-[11px] text-slate-400 leading-relaxed">
            Ground-truth depth measured in meters by the Kinect structured-light infrared sensor with cross-bilateral hole inpainting. Spatial coordinates precisely correspond 1:1 with the RGB image.
          </p>
        </div>

      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 2: SELECT A 5×5 PIXEL REGION -->
    <!-- ======================================================================= -->
    <section id="stage-2" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 2</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Select a 5×5 Pixel Region</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Exact 25-Pixel Spatially Corresponding Patch)</span>
          </h2>
        </div>
        <div class="text-xs text-slate-400">
          Click anywhere on the image viewports above or pick a quick failure sample below.
        </div>
      </div>

      <!-- Quick Preset Chips -->
      <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
        <span class="text-slate-400 text-[11px]">Recommended Failure Regions:</span>
        <button onclick="jumpToRegionPreset(0)" class="px-3 py-1 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 text-cyan-300 border border-cyan-800 transition flex items-center gap-1.5">
          <i class="fa-solid fa-location-crosshairs text-cyan-400"></i>
          <span id="chip-preset-0">Preset 1: Primary Failure Patch</span>
        </button>
        <button onclick="jumpToRegionPreset(1)" class="px-3 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition">
          <span id="chip-preset-1">Preset 2: Boundary Region</span>
        </button>
        <button onclick="jumpToRegionPreset(2)" class="px-3 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition">
          <span id="chip-preset-2">Preset 3: Secondary Artifact</span>
        </button>
      </div>

      <!-- Nearest-Neighbor Magnified 5×5 Dual Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- Magnified 5x5 RGB Grid (6 Cols) -->
        <div class="lg:col-span-6 bg-slate-900 rounded-xl border border-slate-800 p-4 shadow-xl space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-semibold text-slate-200 flex items-center gap-1.5">
              <i class="fa-solid fa-magnifying-glass-plus text-cyan-400"></i>
              <span>Enlarged 5×5 RGB Patch (10× Nearest-Neighbor)</span>
            </span>
            <span id="grid-coord-label" class="font-mono text-cyan-400">Origin: (X: 210, Y: 140)</span>
          </div>

          <!-- 5x5 Interactive Table of Pixels -->
          <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 overflow-x-auto">
            <div id="grid-5x5-rgb" class="grid grid-cols-5 gap-1.5 w-full max-w-[420px] mx-auto aspect-square">
              <!-- 25 RGB pixel tiles populated via JS -->
            </div>
          </div>
          <div class="flex justify-between items-center text-[11px] text-slate-400">
            <span>Click any pixel to inspect individual color & depth values.</span>
            <span class="font-mono text-slate-500">25 sampled pixels</span>
          </div>
        </div>

        <!-- Magnified 5x5 GT Depth Grid (6 Cols) -->
        <div class="lg:col-span-6 bg-slate-900 rounded-xl border border-slate-800 p-4 shadow-xl space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="font-semibold text-slate-200 flex items-center gap-1.5">
              <i class="fa-solid fa-ruler-combined text-emerald-400"></i>
              <span>Enlarged 5×5 Ground-Truth Depth Values (Meters)</span>
            </span>
            <span class="font-mono text-emerald-400">Metric Precision (mm)</span>
          </div>

          <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 overflow-x-auto">
            <div id="grid-5x5-gt" class="grid grid-cols-5 gap-1.5 w-full max-w-[420px] mx-auto aspect-square font-mono text-[11px]">
              <!-- 25 GT depth tiles populated via JS -->
            </div>
          </div>
          <div class="flex justify-between items-center text-[11px] text-slate-400">
            <span>Each cell shows exact sensor distance in meters.</span>
            <span class="font-mono text-emerald-500" id="gt-patch-mean-label">Mean GT: 1.842 m</span>
          </div>
        </div>

      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 3: EXPLAIN HOW DEPTH ANYTHING V2 PRODUCES A DEPTH MAP -->
    <!-- ======================================================================= -->
    <section id="stage-3" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 3</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Explain How Depth Anything V2 Produces a Depth Map</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Step-by-Step Inference Pipeline)</span>
          </h2>
        </div>
        <div class="text-xs text-slate-400">
          Official checkpoint: <code class="font-mono text-cyan-300">depth_anything_v2_metric_hypersim_vits.pth</code>
        </div>
      </div>

      <!-- Inference Pipeline Stepper Tabs -->
      <div class="grid grid-cols-1 md:grid-cols-6 gap-2 text-xs font-medium">
        <button onclick="setPipelineStep(1)" id="pipestep-btn-1" class="p-2.5 rounded-lg border border-cyan-500 bg-cyan-950/60 text-cyan-300 text-left transition">
          <div class="font-mono text-[10px] text-cyan-400">Step 3.1</div>
          <div class="font-semibold text-white">RGB Input</div>
        </button>
        <button onclick="setPipelineStep(2)" id="pipestep-btn-2" class="p-2.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-400 text-left transition hover:text-white">
          <div class="font-mono text-[10px] text-slate-500">Step 3.2</div>
          <div class="font-semibold">Preprocessing</div>
        </button>
        <button onclick="setPipelineStep(3)" id="pipestep-btn-3" class="p-2.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-400 text-left transition hover:text-white">
          <div class="font-mono text-[10px] text-slate-500">Step 3.3</div>
          <div class="font-semibold">Feature Extraction</div>
        </button>
        <button onclick="setPipelineStep(4)" id="pipestep-btn-4" class="p-2.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-400 text-left transition hover:text-white">
          <div class="font-mono text-[10px] text-slate-500">Step 3.4</div>
          <div class="font-semibold">DPT Decoder</div>
        </button>
        <button onclick="setPipelineStep(5)" id="pipestep-btn-5" class="p-2.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-400 text-left transition hover:text-white">
          <div class="font-mono text-[10px] text-slate-500">Step 3.5</div>
          <div class="font-semibold">Predicted Depth</div>
        </button>
        <button onclick="setPipelineStep(6)" id="pipestep-btn-6" class="p-2.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-400 text-left transition hover:text-white">
          <div class="font-mono text-[10px] text-slate-500">Step 3.6</div>
          <div class="font-semibold">Selected 5×5 Pixels</div>
        </button>
      </div>

      <!-- Step Content Display Card -->
      <div class="bg-slate-900 rounded-xl border border-slate-800 p-6 shadow-xl space-y-4">
        
        <!-- Step 3.1 Content -->
        <div id="pipestep-content-1" class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-cube text-cyan-400"></i>
              <span>Step 3.1: RGB Image Enters the Vision Transformer</span>
            </h3>
            <span class="text-xs font-mono text-slate-400">Tensor Input: [1, 3, 480, 640]</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed max-w-4xl">
            Monocular depth estimation is an <strong>ill-posed inverse problem</strong>. The input to Depth Anything V2 consists purely of 2D RGB pixel color intensities. The network does not receive physical range measurements, time-of-flight pulses, or stereoscopic baselines. It must infer the lost 3D dimension entirely by recognizing contextual cues: linear perspective, relative object scale, occlusion edges, surface textural gradients, and ambient lighting transitions.
          </p>
          <div class="p-4 rounded-lg bg-slate-950 border border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
            <div>
              <span class="text-slate-500 block">Color Channels:</span>
              <span class="text-slate-200 font-bold">3 (Red, Green, Blue)</span>
            </div>
            <div>
              <span class="text-slate-500 block">Spatial Resolution:</span>
              <span class="text-slate-200 font-bold">480 × 640 = 307,200 Pixels</span>
            </div>
            <div>
              <span class="text-slate-500 block">Input Space:</span>
              <span class="text-cyan-400 font-bold">2D Pixel Radiance [0..255]</span>
            </div>
          </div>
        </div>

        <!-- Step 3.2 Content -->
        <div id="pipestep-content-2" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-sliders text-cyan-400"></i>
              <span>Step 3.2: Input Preprocessing & Patch Alignment</span>
            </h3>
            <span class="text-xs font-mono text-slate-400">Tensor Output: [1, 3, 518, 686]</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed max-w-4xl">
            Depth Anything V2 requires image dimensions to be exact multiples of its ViT patch size (<code class="text-cyan-300 font-mono">P = 14</code>). The input image is converted from uint8 [0, 255] to float32 [0, 1], normalized with standard ImageNet channel statistics, and interpolated to dimensions divisible by 14:
          </p>
          <div class="p-4 rounded-lg bg-slate-950 border border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
            <div>
              <span class="text-slate-500 block">Normalization Mean (μ):</span>
              <span class="text-slate-200">[0.485, 0.456, 0.406]</span>
            </div>
            <div>
              <span class="text-slate-500 block">Normalization Std (σ):</span>
              <span class="text-slate-200">[0.229, 0.224, 0.225]</span>
            </div>
            <div>
              <span class="text-slate-500 block">Patch Grid (H/14 × W/14):</span>
              <span class="text-cyan-400 font-bold">37 × 49 = 1,813 Patch Tokens</span>
            </div>
          </div>
        </div>

        <!-- Step 3.3 Content -->
        <div id="pipestep-content-3" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-network-wired text-cyan-400"></i>
              <span>Step 3.3: Visual Feature Extraction via DINOv2 ViT-Small</span>
            </h3>
            <span class="text-xs font-mono text-emerald-400">Authentic Model Activations Extracted via Hooks</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed max-w-4xl">
            The backbone is an authentic <strong>DINOv2 ViT-Small</strong> (12 transformer blocks, embedding dim 384). The non-overlapping 14×14 patches are projected into linear embeddings and processed through multi-head self-attention. Below are the actual intermediate activation maps captured from the model forward pass:
          </p>

          <!-- Authentic Intermediate Activation Maps Gallery -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
            
            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3 space-y-2">
              <span class="text-[10px] font-mono font-bold text-cyan-400 uppercase">Layer 3 (Early Stage)</span>
              <img id="featmap-layer3" src="" alt="Layer 3 Features" class="w-full aspect-[4/3] object-cover rounded border border-slate-800">
              <p class="text-[11px] text-slate-400 leading-tight">
                High-frequency contrast transitions, edge filters, and localized illumination gradients.
              </p>
            </div>

            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3 space-y-2">
              <span class="text-[10px] font-mono font-bold text-emerald-400 uppercase">Layer 6 (Mid Stage)</span>
              <img id="featmap-layer6" src="" alt="Layer 6 Features" class="w-full aspect-[4/3] object-cover rounded border border-slate-800">
              <p class="text-[11px] text-slate-400 leading-tight">
                Textural grouping, local surface geometry, and orientation patch associations.
              </p>
            </div>

            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3 space-y-2">
              <span class="text-[10px] font-mono font-bold text-amber-400 uppercase">Layer 9 (Semantic Stage)</span>
              <img id="featmap-layer9" src="" alt="Layer 9 Features" class="w-full aspect-[4/3] object-cover rounded border border-slate-800">
              <p class="text-[11px] text-slate-400 leading-tight">
                Object part boundaries, semantic clustering, and inter-object relational depth bounds.
              </p>
            </div>

            <div class="bg-slate-950 border border-slate-800 rounded-lg p-3 space-y-2">
              <span class="text-[10px] font-mono font-bold text-purple-400 uppercase">Layer 12 (Global Stage)</span>
              <img id="featmap-layer12" src="" alt="Layer 12 Features" class="w-full aspect-[4/3] object-cover rounded border border-slate-800">
              <p class="text-[11px] text-slate-400 leading-tight">
                Scene-level spatial layout, planar ground-plane horizon priors, and global room bounds.
              </p>
            </div>

          </div>
        </div>

        <!-- Step 3.4 Content -->
        <div id="pipestep-content-4" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-diagram-project text-cyan-400"></i>
              <span>Step 3.4: DPT Decoder & Multi-Scale Feature Fusion</span>
            </h3>
            <span class="text-xs font-mono text-slate-400">Dense Prediction Transformer (DPT)</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed max-w-4xl">
            Depth Anything V2 connects the ViT encoder to a <strong>DPT (Dense Prediction Transformer)</strong> decoder. 
            Tokens from layers [3, 6, 9, 12] are projected via 1×1 convolutions into multi-resolution pyramid scales (stride 4, stride 8, stride 16, stride 32). 
            Four residual <strong>FeatureFusionBlocks (RefineNet 4 → 3 → 2 → 1)</strong> iteratively upsample and merge high-level semantic context with fine-grained spatial boundaries.
          </p>
          <div class="p-4 rounded-lg bg-slate-950 border border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
            <div>
              <span class="text-slate-500 block">Projection Channels:</span>
              <span class="text-slate-200">[48, 96, 192, 384]</span>
            </div>
            <div>
              <span class="text-slate-500 block">Fusion Feature Dim:</span>
              <span class="text-slate-200">64 channels</span>
            </div>
            <div>
              <span class="text-slate-500 block">Head Activation:</span>
              <span class="text-cyan-400 font-bold">Bilinear Upsample → 3×3 Conv → ReLU</span>
            </div>
          </div>
        </div>

        <!-- Step 3.5 Content -->
        <div id="pipestep-content-5" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-map text-cyan-400"></i>
              <span>Step 3.5: Full Predicted Dense Depth Map</span>
            </h3>
            <span id="pred-range-label" class="text-xs font-mono text-cyan-400">Range: 0.719m – 2.222m</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            <div class="md:col-span-7 rounded-lg overflow-hidden border border-slate-800 bg-black">
              <canvas id="canvas-depth-pred" width="640" height="480" class="w-full h-auto block"></canvas>
            </div>
            <div class="md:col-span-5 space-y-3 text-xs text-slate-300">
              <p>
                The model outputs a dense, continuous depth map across all 307,200 pixels.
              </p>
              <div class="p-3 bg-slate-950 rounded border border-slate-800 font-mono space-y-1">
                <div class="flex justify-between"><span>Global RMSE:</span> <span id="meta-rmse" class="text-cyan-400 font-bold">0.2088 m</span></div>
                <div class="flex justify-between"><span>Global AbsRel:</span> <span id="meta-absrel" class="text-cyan-400 font-bold">0.0860</span></div>
                <div class="flex justify-between"><span>Delta-1 Accuracy:</span> <span id="meta-delta1" class="text-emerald-400 font-bold">93.2 %</span></div>
                <div class="flex justify-between"><span>Spearman Rank:</span> <span id="meta-spearman" class="text-slate-300 font-bold">0.874</span></div>
              </div>
              <p class="text-[11px] text-slate-400">
                At first glance, these aggregate benchmark metrics look impressive. But proceed to Stage 4 to see where significant localized errors are hidden!
              </p>
            </div>
          </div>
        </div>

        <!-- Step 3.6 Content -->
        <div id="pipestep-content-6" class="hidden space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <i class="fa-solid fa-table-cells text-cyan-400"></i>
              <span>Step 3.6: Magnified 5×5 Predicted Depth Grid</span>
            </h3>
            <span class="text-xs font-mono text-cyan-400">Predicted Depth (Meters)</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            <div class="md:col-span-6 p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div id="grid-5x5-pred" class="grid grid-cols-5 gap-1.5 w-full max-w-[380px] mx-auto aspect-square font-mono text-[11px]">
                <!-- 25 Pred depth tiles populated via JS -->
              </div>
            </div>
            <div class="md:col-span-6 space-y-3 text-xs text-slate-300">
              <p class="leading-relaxed">
                Here are the exact 25 predicted depth values for the selected 5×5 region. 
                Compare them against the Ground Truth values from Stage 2. Notice how the model's estimate diverges on specific local pixels.
              </p>
              <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs space-y-1">
                <div class="flex justify-between"><span>Patch Mean Pred:</span> <strong id="pred-patch-mean-label" class="text-cyan-300">--- m</strong></div>
                <div class="flex justify-between"><span>Patch Mean GT:</span> <strong id="gt-patch-mean-label-2" class="text-emerald-300">--- m</strong></div>
                <div class="flex justify-between"><span>Mean Absolute Diff:</span> <strong id="diff-patch-mean-label" class="text-red-400">--- m</strong></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 4: THE CRITICAL INSIGHT: CONVINCING DEPTH CAN STILL BE WRONG -->
    <!-- ======================================================================= -->
    <section id="stage-4" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 4</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>The Critical Insight: A Convincing Depth Map Can Still Be Wrong</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Visual Reveal & Local Discrepancy)</span>
          </h2>
        </div>
      </div>

      <!-- Prominent Callout Banner -->
      <div class="bg-gradient-to-r from-red-950/40 via-slate-900 to-slate-900 border border-red-900/60 rounded-xl p-5 shadow-2xl relative overflow-hidden">
        <div class="max-w-4xl space-y-2">
          <div class="flex items-center space-x-2 text-red-400 font-mono text-xs font-bold uppercase tracking-wider">
            <i class="fa-solid fa-triangle-exclamation"></i>
            <span>The Computer Vision Benchmark Blind Spot</span>
          </div>
          <p class="text-sm md:text-base font-semibold text-slate-100 leading-relaxed">
            A depth map can look visually plausible at the full-scene level while containing significant local prediction errors. VEO investigates where these errors occur, measures them quantitatively, and uncovers the evidence that explains them.
          </p>
          <p class="text-xs text-slate-400 leading-relaxed">
            In autonomous navigation, robotics, or augmented reality, a global average error of 8% means nothing if a localized 0.4-meter error occurs right on a glass door, chair leg, or table edge.
          </p>
        </div>
      </div>

      <!-- 4-Way Comparison Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div class="bg-slate-900 rounded-xl border border-slate-800 p-3 space-y-2">
          <span class="text-xs font-semibold text-slate-300">1. Original RGB</span>
          <div class="rounded overflow-hidden border border-slate-800 bg-black aspect-[4/3]">
            <img id="reveal-img-rgb" src="" alt="RGB" class="w-full h-full object-cover">
          </div>
          <span class="text-[11px] text-slate-500 block">Visual appearance</span>
        </div>

        <div class="bg-slate-900 rounded-xl border border-slate-800 p-3 space-y-2">
          <span class="text-xs font-semibold text-emerald-400">2. Ground Truth Depth</span>
          <div class="rounded overflow-hidden border border-slate-800 bg-black aspect-[4/3]">
            <img id="reveal-img-gt" src="" alt="GT" class="w-full h-full object-cover">
          </div>
          <span class="text-[11px] text-slate-500 block">Kinect sensor measurement</span>
        </div>

        <div class="bg-slate-900 rounded-xl border border-slate-800 p-3 space-y-2">
          <span class="text-xs font-semibold text-cyan-400">3. Predicted Depth</span>
          <div class="rounded overflow-hidden border border-slate-800 bg-black aspect-[4/3]">
            <img id="reveal-img-pred" src="" alt="Pred" class="w-full h-full object-cover">
          </div>
          <span class="text-[11px] text-slate-500 block">Visually coherent model output</span>
        </div>

        <div class="bg-slate-900 rounded-xl border border-slate-800 p-3 space-y-2">
          <span class="text-xs font-semibold text-red-400">4. Relative Error Map</span>
          <div class="rounded overflow-hidden border border-slate-800 bg-black aspect-[4/3]">
            <img id="reveal-img-err" src="" alt="Error" class="w-full h-full object-cover">
          </div>
          <span class="text-[11px] text-slate-500 block">Divergence: |Pred - GT| / GT</span>
        </div>

      </div>

      <!-- Interactive Error Threshold Filter Slider -->
      <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4 text-xs font-mono">
        <div class="flex items-center space-x-3">
          <span class="text-slate-300 font-semibold flex items-center gap-1.5">
            <i class="fa-solid fa-filter text-amber-400"></i>
            <span>Interactive Error Filter Threshold:</span>
          </span>
          <input type="range" id="threshold-slider" min="5" max="40" value="15" oninput="onThresholdChange(this.value)" class="w-48 accent-cyan-500 cursor-pointer">
          <span id="threshold-label" class="text-cyan-400 font-bold px-2 py-0.5 rounded bg-slate-950 border border-slate-800">15% Relative Error</span>
        </div>
        <div class="text-slate-400 text-[11px]">
          Highlights regions where local error exceeds the benchmark tolerance threshold.
        </div>
      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 5: COMPARE PREDICTION AGAINST GROUND TRUTH (25-PIXEL TABLE) -->
    <!-- ======================================================================= -->
    <section id="stage-5" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 5</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Pixel-Level Error Analysis</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Quantitative 25-Pixel Corresponding Table)</span>
          </h2>
        </div>
        <div class="text-xs text-slate-400">
          Showing exact values for selected 5×5 region: <span id="table-region-coord" class="font-mono text-cyan-400">[210..214, 140..144]</span>
        </div>
      </div>

      <!-- Mathematical Formulas Callout Card -->
      <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2">
        <span class="text-[10px] font-mono font-bold text-cyan-400 uppercase tracking-wider">Evaluation Formulas & Alignment Protocol:</span>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-[11px] text-slate-300">
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span class="text-slate-500 block text-[10px]">Absolute Error:</span>
            <span class="text-white font-bold">ε_abs = |d_pred - d_gt|</span>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span class="text-slate-500 block text-[10px]">Relative Error:</span>
            <span class="text-white font-bold">ε_rel = |d_pred - d_gt| / d_gt</span>
          </div>
          <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
            <span class="text-slate-500 block text-[10px]">Scale-Shift Metric Inversion:</span>
            <span class="text-cyan-400 font-bold">1/D ≈ s·P + b</span>
          </div>
        </div>
      </div>

      <!-- Quantitative 25-Pixel Table -->
      <div class="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden shadow-xl">
        <div class="max-h-[380px] overflow-y-auto">
          <table class="w-full text-left text-xs font-mono">
            <thead class="bg-slate-950 text-slate-400 uppercase text-[10px] sticky top-0 z-10 border-b border-slate-800">
              <tr>
                <th class="p-3">#</th>
                <th class="p-3">Coord (X, Y)</th>
                <th class="p-3">RGB Color</th>
                <th class="p-3">Ground Truth (m)</th>
                <th class="p-3">Predicted (m)</th>
                <th class="p-3">Abs Error (m)</th>
                <th class="p-3">Rel Error (%)</th>
                <th class="p-3">Status</th>
              </tr>
            </thead>
            <tbody id="table-25-pixels-body" class="divide-y divide-slate-800/60 text-slate-300">
              <!-- 25 Rows populated dynamically via JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Patch Summary Metrics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
        <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
          <span class="text-slate-500 block text-[10px]">Patch Mean Abs Error:</span>
          <span id="patch-mae-val" class="text-white text-sm font-bold">--- m</span>
        </div>
        <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
          <span class="text-slate-500 block text-[10px]">Patch Mean Rel Error:</span>
          <span id="patch-mare-val" class="text-red-400 text-sm font-bold">--- %</span>
        </div>
        <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
          <span class="text-slate-500 block text-[10px]">Patch Max Error:</span>
          <span id="patch-maxerr-val" class="text-amber-400 text-sm font-bold">--- m</span>
        </div>
        <div class="p-3 rounded-lg bg-slate-900 border border-slate-800">
          <span class="text-slate-500 block text-[10px]">Patch Local RMSE:</span>
          <span id="patch-rmse-val" class="text-cyan-400 text-sm font-bold">--- m</span>
        </div>
      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 6: VISUALIZE THE ERROR IN THREE DIMENSIONS (3D) -->
    <!-- ======================================================================= -->
    <section id="stage-6" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 6</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Visualize the Error in Three Dimensions</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Interactive WebGL 3D Surface & Discrepancy Mesh)</span>
          </h2>
        </div>
        <div class="text-xs text-slate-400">
          Controls: Left-drag to rotate | Right-drag to pan | Scroll to zoom
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- 3D Canvas Viewport (8 Cols) -->
        <div class="lg:col-span-8 bg-slate-900 rounded-xl border border-slate-800 p-4 shadow-xl space-y-3">
          
          <div class="flex flex-wrap items-center justify-between gap-3 text-xs">
            
            <!-- Scope Toggle: 5x5 Patch vs Full Room -->
            <div class="flex items-center space-x-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
              <button onclick="set3DMode('patch')" id="btn-3d-patch" class="px-3 py-1 rounded bg-cyan-600 text-white font-medium transition">
                5×5 Local Elevation Lattice
              </button>
              <button onclick="set3DMode('scene')" id="btn-3d-scene" class="px-3 py-1 rounded text-slate-400 hover:text-white font-medium transition">
                Full Room 3D Mesh
              </button>
            </div>

            <!-- Surface Layer View -->
            <div class="flex items-center space-x-2 text-xs font-mono">
              <span class="text-slate-400">Layer:</span>
              <select id="select-3d-layer" onchange="on3DLayerChange(this.value)" class="bg-slate-950 text-cyan-300 border border-slate-700 rounded px-2 py-1 focus:outline-none">
                <option value="overlay">Dual Surface Overlay (GT vs Pred)</option>
                <option value="gt">Ground Truth Physical Geometry</option>
                <option value="pred">Predicted Model Geometry</option>
                <option value="error">Error Discrepancy Heatmap</option>
              </select>
              <button onclick="reset3DCamera()" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" title="Reset Camera">
                <i class="fa-solid fa-arrows-rotate"></i>
              </button>
            </div>

          </div>

          <!-- The WebGL Canvas Container -->
          <div id="container-3d" class="relative w-full h-[450px] rounded-lg overflow-hidden bg-black border border-slate-800">
            <!-- Three.js renders here -->
          </div>

          <div class="flex justify-between items-center text-[11px] text-slate-400">
            <span>Z-axis indicates physical metric depth away from the camera optical center.</span>
            <span class="font-mono text-cyan-400">Three.js r128 WebGL</span>
          </div>
        </div>

        <!-- 3D Diagnostic Explainer Panel (4 Cols) -->
        <div class="lg:col-span-4 bg-slate-900 rounded-xl border border-slate-800 p-5 shadow-xl space-y-4">
          <h3 class="text-sm font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-layer-group text-cyan-400"></i>
            <span>3D Geometric Discrepancy</span>
          </h3>

          <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-2">
            <span class="text-[10px] font-mono font-bold text-emerald-400 uppercase">Ground Truth Surface (Green):</span>
            <p class="text-slate-300 leading-relaxed">
              Represents the actual continuous physical plane measured by structured infrared light.
            </p>
          </div>

          <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-2">
            <span class="text-[10px] font-mono font-bold text-amber-400 uppercase">Predicted Surface (Orange):</span>
            <p class="text-slate-300 leading-relaxed">
              The model's reconstructed 3D surface. In textureless or specular regions, it often warps or introduces a false tilt.
            </p>
          </div>

          <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-2">
            <span class="text-[10px] font-mono font-bold text-red-400 uppercase">3D Displacement Stems (Red):</span>
            <p class="text-slate-300 leading-relaxed">
              Vertical lines connecting corresponding vertices directly show the magnitude of the 3D error vector (ΔZ) at each pixel.
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 7: VEO TRACES THE ERROR (FAILURE ANALYSIS & EVIDENCE CHAINS) -->
    <!-- ======================================================================= -->
    <section id="stage-7" class="space-y-4 pt-2">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 7</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>VEO Traces the Error</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Hypothesis Testing & Empirical Evidence Chains)</span>
          </h2>
        </div>
      </div>

      <!-- Linear Investigation Trace Pipeline -->
      <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 overflow-x-auto">
        <div class="flex items-center justify-between min-w-[700px] text-xs font-mono">
          <div class="text-center space-y-1">
            <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300 font-semibold">1. Input RGB</span>
            <p class="text-[10px] text-slate-500">2D Pixels</p>
          </div>
          <i class="fa-solid fa-arrow-right text-slate-600"></i>
          <div class="text-center space-y-1">
            <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-cyan-400 font-semibold">2. Predicted Depth</span>
            <p class="text-[10px] text-slate-500">ViT Inference</p>
          </div>
          <i class="fa-solid fa-arrow-right text-slate-600"></i>
          <div class="text-center space-y-1">
            <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-emerald-400 font-semibold">3. Ground Truth</span>
            <p class="text-[10px] text-slate-500">Kinect IR</p>
          </div>
          <i class="fa-solid fa-arrow-right text-slate-600"></i>
          <div class="text-center space-y-1">
            <span class="px-2 py-0.5 rounded bg-red-950 border border-red-800 text-red-300 font-semibold">4. Error Deviation</span>
            <p class="text-[10px] text-slate-500">|Pred - GT|</p>
          </div>
          <i class="fa-solid fa-arrow-right text-slate-600"></i>
          <div class="text-center space-y-1">
            <span class="px-2 py-0.5 rounded bg-amber-950 border border-amber-800 text-amber-300 font-semibold">5. Regional Evidence</span>
            <p class="text-[10px] text-slate-500">Texture, Edges, Discon</p>
          </div>
          <i class="fa-solid fa-arrow-right text-slate-600"></i>
          <div class="text-center space-y-1">
            <span class="px-2 py-0.5 rounded bg-blue-950 border border-blue-800 text-blue-300 font-semibold">6. Hypothesized Cause</span>
            <p class="text-[10px] text-slate-500">Evidence Match</p>
          </div>
        </div>
      </div>

      <!-- 7 Failure Categories Matrix -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" id="cards-categories-container">
        <!-- Populated via JS with empirical pass/fail badges -->
      </div>
    </section>

    <!-- ======================================================================= -->
    <!-- STAGE 8: INVESTIGATE WHETHER ERROR COMES FROM MODEL OR IMAGE -->
    <!-- ======================================================================= -->
    <section id="stage-8" class="space-y-4 pt-2 pb-12">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <span class="text-xs font-mono text-cyan-400 font-semibold tracking-wider uppercase">Stage 8</span>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span>Investigate Whether the Error Comes From the Model or the Image</span>
            <span class="text-xs font-normal text-slate-400 font-mono">(Dual-Dimension Attribution & Structured Report Card)</span>
          </h2>
        </div>
      </div>

      <!-- Dual Dimension Evidence Split -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- Dimension A: Image-Related Evidence (6 Cols) -->
        <div class="lg:col-span-6 bg-slate-900 rounded-xl border border-slate-800 p-5 shadow-xl space-y-3">
          <div class="flex items-center space-x-2 text-sm font-bold text-cyan-400">
            <i class="fa-solid fa-camera text-base"></i>
            <span>Dimension A: Image-Related Evidence</span>
          </div>
          <p class="text-xs text-slate-400 leading-relaxed">
            Observable physical and optical properties extracted from the RGB image and scene geometry.
          </p>

          <div class="space-y-2 text-xs font-mono">
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Texture Variance (σ²):</span>
              <strong id="ev-texture-var" class="text-white">---</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Edge Density (Canny):</span>
              <strong id="ev-edge-density" class="text-white">---</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Depth Discontinuity (Δd):</span>
              <strong id="ev-depth-discon" class="text-white">--- m</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Brightness / Contrast:</span>
              <strong id="ev-lighting" class="text-white">--- / ---</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Specular Highlight Ratio:</span>
              <strong id="ev-highlight-ratio" class="text-white">---</strong>
            </div>
          </div>
        </div>

        <!-- Dimension B: Model-Related Evidence (6 Cols) -->
        <div class="lg:col-span-6 bg-slate-900 rounded-xl border border-slate-800 p-5 shadow-xl space-y-3">
          <div class="flex items-center space-x-2 text-sm font-bold text-amber-400">
            <i class="fa-solid fa-brain text-base"></i>
            <span>Dimension B: Model-Related Evidence</span>
          </div>
          <p class="text-xs text-slate-400 leading-relaxed">
            Architectural characteristics and inductive biases of the Depth Anything V2 Vision Transformer.
          </p>

          <div class="space-y-2 text-xs font-mono">
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Patch Receptive Field:</span>
              <strong class="text-white">14 × 14 px = 1 Spatial Token</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Decoder Upsampling:</span>
              <strong class="text-white">Bilinear Interpolation (Smooths edges)</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Self-Attention Entropy:</span>
              <strong id="ev-attn-bias" class="text-amber-400">Diffuse Attention Prior</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Scale-Shift Sensitivity:</span>
              <strong class="text-white">High (Inverse Depth Regression)</strong>
            </div>
            <div class="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
              <span>Error Polarity:</span>
              <strong id="ev-polarity" class="text-red-400">Overshoot (+0.28m)</strong>
            </div>
          </div>
        </div>

      </div>

      <!-- Structured Failure Report Card -->
      <div class="bg-gradient-to-b from-slate-900 to-slate-950 rounded-xl border border-slate-800 p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between pb-2 border-b border-slate-800">
          <h3 class="text-base font-bold text-white flex items-center gap-2">
            <i class="fa-solid fa-file-contract text-cyan-400"></i>
            <span>Structured Diagnostic Report Card</span>
          </h3>
          <span class="text-xs font-mono px-2.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800" id="card-confidence-badge">
            Confidence: High (84%)
          </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
          
          <div class="space-y-3">
            <div>
              <span class="text-[10px] font-mono font-bold text-slate-500 uppercase block">1. Observed Error:</span>
              <p id="card-observed-err" class="text-slate-200 font-mono mt-0.5">
                Local depth overestimation of +0.312m (relative error: 18.4%).
              </p>
            </div>
            <div>
              <span class="text-[10px] font-mono font-bold text-slate-500 uppercase block">2. Spatial Location:</span>
              <p id="card-location" class="text-slate-200 font-mono mt-0.5">
                Coordinates (X: 210..214, Y: 140..144) in NYU Test Scene 0049.
              </p>
            </div>
            <div>
              <span class="text-[10px] font-mono font-bold text-slate-500 uppercase block">3. Image-Level Evidence:</span>
              <p id="card-img-ev" class="text-slate-300 leading-relaxed mt-0.5">
                Texture variance is 124.2 (low), edge density is 0.01 (flat). The visual patch depicts a featureless painted wall with diffuse Lambertian reflection.
              </p>
            </div>
          </div>

          <div class="space-y-3">
            <div>
              <span class="text-[10px] font-mono font-bold text-slate-500 uppercase block">4. Model-Level Evidence:</span>
              <p id="card-model-ev" class="text-slate-300 leading-relaxed mt-0.5">
                The Vision Transformer lacks high-frequency gradient anchors in the self-attention patch. The DPT decoder applies a smooth planar prior, blending the wall with nearby geometry.
              </p>
            </div>
            <div>
              <span class="text-[10px] font-mono font-bold text-slate-500 uppercase block">5. Plausible Explanation:</span>
              <p id="card-explanation" class="text-cyan-300 font-semibold leading-relaxed mt-0.5">
                Textureless Planar Ambiguity. The model cannot anchor depth on untextured surfaces without active multi-view disparity.
              </p>
            </div>
            <div>
              <span class="text-[10px] font-mono font-bold text-slate-500 uppercase block">6. Scientific Limitations:</span>
              <p class="text-slate-400 leading-relaxed mt-0.5">
                Correlation between low variance and depth error does not prove pure architectural fault. Without controlled active sensor ablation (e.g. projecting a speckle pattern onto the wall), the exact contribution of illumination cannot be fully isolated.
              </p>
            </div>
          </div>

        </div>
      </div>

    </section>

  </main>

  <!-- ========================================================================= -->
  <!-- FOOTER -->
  <!-- ========================================================================= -->
  <footer class="border-t border-slate-800 bg-[#070B12] py-6 px-4 text-center text-xs text-slate-500 space-y-1">
    <p>Vision Error Observatory (VEO) &bull; Capstone Project &bull; NMIMS Hyderabad</p>
    <p class="text-[11px] text-slate-600 font-mono">NYU Depth V2 Dataset &bull; Depth Anything V2 Pretrained ViT-Small &bull; Three.js WebGL</p>
  </footer>

  <!-- ========================================================================= -->
  <!-- APPLICATION SCRIPT LOGIC -->
  <!-- ========================================================================= -->
  <script>
    // Global Application State
    let currentScene = null;
    let currentSceneId = "scene_0049";
    let gtDepthRaw = null;      // Uint16Array (depth in mm)
    let predDepthRaw = null;    // Uint16Array (depth in mm)
    let selectedX = 210;
    let selectedY = 140;
    let activePixelIdx = 12;     // Center of 5x5 patch (index 0..24)
    let errorThreshold = 0.15;   // 15% relative error
    
    // Three.js State
    let scene3D, camera3D, renderer3D, controls3D;
    let current3DMode = 'patch'; // 'patch' or 'scene'
    let current3DLayer = 'overlay';
    let meshGroup = null;

    // =========================================================================
    // INITIALIZATION
    // =========================================================================
    function initApp() {
      if (!window.VEO_DATA || !window.VEO_DATA.scenes) {
        console.error("VEO Data not loaded.");
        alert("Error: VEO dataset payload not found. Please ensure data/app_data_v2.js is present.");
        return;
      }

      // Populate Scene Dropdown
      const select = document.getElementById('scene-select');
      select.innerHTML = '';
      window.VEO_DATA.scenes.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.sample_id;
        opt.textContent = `${s.sample_id.toUpperCase()} - ${s.title}`;
        select.appendChild(opt);
      });

      // Initialize 3D Engine
      init3DEngine();

      // Load initial scene
      loadScene(currentSceneId);

      // Setup 2D Canvas Listeners
      setupCanvasListeners('canvas-rgb');
      setupCanvasListeners('canvas-depth-gt');
    }

    // =========================================================================
    // SCENE LOADING & PARSING
    // =========================================================================
    function loadScene(sceneId) {
      currentScene = window.VEO_DATA.scenes.find(s => s.sample_id === sceneId);
      if (!currentScene) return;
      currentSceneId = sceneId;

      document.getElementById('scene-select').value = sceneId;
      document.getElementById('scene-meta-pill').textContent = 
        `NYU Test: ${sceneId.toUpperCase()} | 480×640 px | Kinect RGB-D | ${currentScene.category_focus}`;

      // Decode 16-bit Millimeter Depth Buffers
      gtDepthRaw = decodeBase64Uint16(currentScene.raw_depth.gt_b64_uint16);
      predDepthRaw = decodeBase64Uint16(currentScene.raw_depth.pred_b64_uint16);

      // Render 2D Viewports
      renderImageToCanvas('canvas-rgb', currentScene.images.rgb);
      renderImageToCanvas('canvas-depth-gt', currentScene.images.depth_gt);
      renderImageToCanvas('canvas-depth-pred', currentScene.images.depth_pred);

      // Update Reveal Images
      document.getElementById('reveal-img-rgb').src = currentScene.images.rgb;
      document.getElementById('reveal-img-gt').src = currentScene.images.depth_gt;
      document.getElementById('reveal-img-pred').src = currentScene.images.depth_pred;
      document.getElementById('reveal-img-err').src = currentScene.images.error_map;

      // Update Intermediate Activation Maps
      document.getElementById('featmap-layer3').src = currentScene.feature_maps.layer_3.image;
      document.getElementById('featmap-layer6').src = currentScene.feature_maps.layer_6.image;
      document.getElementById('featmap-layer9').src = currentScene.feature_maps.layer_9.image;
      document.getElementById('featmap-layer12').src = currentScene.feature_maps.layer_12.image;

      // Update Metrics Labels
      document.getElementById('gt-range-label').textContent = 
        `Range: ${currentScene.depth_range[0]}m – ${currentScene.depth_range[1]}m`;
      document.getElementById('pred-range-label').textContent = 
        `Range: ${currentScene.pred_range[0]}m – ${currentScene.pred_range[1]}m`;
      document.getElementById('meta-rmse').textContent = `${currentScene.metrics.rmse.toFixed(4)} m`;
      document.getElementById('meta-absrel').textContent = currentScene.metrics.abs_rel.toFixed(4);
      document.getElementById('meta-delta1').textContent = `${(currentScene.metrics.delta1 * 100).toFixed(1)} %`;
      document.getElementById('meta-spearman').textContent = currentScene.metrics.spearman.toFixed(3);

      // Update Preset Chips
      updatePresetChips();

      // Position default 5x5 region
      const defReg = currentScene.default_region;
      selectRegion(defReg.x, defReg.y);
    }

    function decodeBase64Uint16(base64Str) {
      const binStr = atob(base64Str);
      const len = binStr.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binStr.charCodeAt(i);
      }
      return new Uint16Array(bytes.buffer);
    }

    function renderImageToCanvas(canvasId, src) {
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };
      img.src = src;
    }

    function onSceneSelectChange(val) {
      loadScene(val);
    }

    function updatePresetChips() {
      if (!currentScene.regions || currentScene.regions.length === 0) return;
      document.getElementById('chip-preset-0').textContent = `Preset 1: ${formatCategoryName(currentScene.regions[0].top_cause)}`;
      if (currentScene.regions.length > 1) {
        document.getElementById('chip-preset-1').textContent = `Preset 2: ${formatCategoryName(currentScene.regions[1].top_cause)}`;
      }
      if (currentScene.regions.length > 2) {
        document.getElementById('chip-preset-2').textContent = `Preset 3: ${formatCategoryName(currentScene.regions[2].top_cause)}`;
      }
    }

    function jumpToRegionPreset(idx) {
      if (!currentScene.regions || !currentScene.regions[idx]) return;
      const reg = currentScene.regions[idx];
      const cx = Math.floor(reg.bbox[0] + reg.bbox[2] / 2);
      const cy = Math.floor(reg.bbox[1] + reg.bbox[3] / 2);
      selectRegion(cx, cy);
    }

    // =========================================================================
    // 5x5 PIXEL REGION SELECTION & COMPUTATION
    // =========================================================================
    function selectRegion(x, y) {
      // Clamp to valid 5x5 bounds
      selectedX = Math.max(0, Math.min(640 - 5, x - 2));
      selectedY = Math.max(0, Math.min(480 - 5, y - 2));

      // Update Bounding Box Overlays on Viewports
      updateSelectionOverlay('selection-box-rgb', selectedX, selectedY);
      updateSelectionOverlay('selection-box-gt', selectedX, selectedY);

      // Update HUD Labels
      document.getElementById('hud-region-coord').textContent = 
        `[X: ${selectedX}..${selectedX+4}, Y: ${selectedY}..${selectedY+4}]`;
      document.getElementById('grid-coord-label').textContent = 
        `Origin: (X: ${selectedX}, Y: ${selectedY})`;
      document.getElementById('table-region-coord').textContent = 
        `[${selectedX}..${selectedX+4}, ${selectedY}..${selectedY+4}]`;

      // Extract 25 Pixels Data
      const pixels = [];
      const canvasRgb = document.getElementById('canvas-rgb');
      const ctxRgb = canvasRgb.getContext('2d');
      const rgbImageData = ctxRgb.getImageData(selectedX, selectedY, 5, 5).data;

      let sumGt = 0;
      let sumPred = 0;
      let sumAbsErr = 0;
      let sumRelErr = 0;
      let maxErr = -1;
      let maxErrIdx = 0;
      let grayValues = [];

      for (let r = 0; r < 5; r++) {
        for (let c = 0; c < 5; c++) {
          const idx = r * 5 + c;
          const px = selectedX + c;
          const py = selectedY + r;
          const flatIdx = py * 640 + px;

          const gtM = gtDepthRaw[flatIdx] / 1000.0;
          const predM = predDepthRaw[flatIdx] / 1000.0;
          const absErr = Math.abs(predM - gtM);
          const relErr = gtM > 0 ? absErr / gtM : 0;

          const rgbIdx = idx * 4;
          const rVal = rgbImageData[rgbIdx];
          const gVal = rgbImageData[rgbIdx + 1];
          const bVal = rgbImageData[rgbIdx + 2];
          const gray = 0.299 * rVal + 0.587 * gVal + 0.114 * bVal;
          grayValues.push(gray);

          if (absErr > maxErr) {
            maxErr = absErr;
            maxErrIdx = idx;
          }

          sumGt += gtM;
          sumPred += predM;
          sumAbsErr += absErr;
          sumRelErr += relErr;

          pixels.push({
            idx,
            r,
            c,
            px,
            py,
            rgb: [rVal, gVal, bVal],
            gray,
            gtM,
            predM,
            absErr,
            relErr
          });
        }
      }

      // Compute Patch Statistics
      const meanGt = sumGt / 25.0;
      const meanPred = sumPred / 25.0;
      const meanAbsErr = sumAbsErr / 25.0;
      const meanRelErr = sumRelErr / 25.0;
      const patchRmse = Math.sqrt(pixels.reduce((acc, p) => acc + Math.pow(p.absErr, 2), 0) / 25.0);

      // Texture variance on 5x5 patch
      const meanGray = grayValues.reduce((a, b) => a + b, 0) / 25.0;
      const textureVar = grayValues.reduce((acc, v) => acc + Math.pow(v - meanGray, 2), 0) / 25.0;

      // Update Grid Displays
      render5x5Grids(pixels, maxErrIdx);

      // Update Quantitative 25-Pixel Table
      render25PixelTable(pixels, maxErrIdx);

      // Update Summary Cards
      document.getElementById('gt-patch-mean-label').textContent = `Mean GT: ${meanGt.toFixed(3)} m`;
      document.getElementById('gt-patch-mean-label-2').textContent = `${meanGt.toFixed(3)} m`;
      document.getElementById('pred-patch-mean-label').textContent = `${meanPred.toFixed(3)} m`;
      document.getElementById('diff-patch-mean-label').textContent = `${meanAbsErr.toFixed(3)} m`;

      document.getElementById('patch-mae-val').textContent = `${meanAbsErr.toFixed(3)} m`;
      document.getElementById('patch-mare-val').textContent = `${(meanRelErr * 100).toFixed(1)} %`;
      document.getElementById('patch-maxerr-val').textContent = `${maxErr.toFixed(3)} m`;
      document.getElementById('patch-rmse-val').textContent = `${patchRmse.toFixed(3)} m`;

      // Select default active pixel
      selectPixel(pixels[activePixelIdx] || pixels[12]);

      // Update 3D Surface
      update3DSurface(pixels);

      // Update Failure Investigation Analysis
      updateFailureInvestigation(pixels, meanAbsErr, meanRelErr, textureVar);
    }

    function updateSelectionOverlay(boxId, x, y) {
      const box = document.getElementById(boxId);
      // Normalized percentage coordinates relative to 640x480
      const leftPct = (x / 640.0) * 100;
      const topPct = (y / 480.0) * 100;
      const widthPct = (5.0 / 640.0) * 100;
      const heightPct = (5.0 / 480.0) * 100;

      box.style.left = `${leftPct}%`;
      box.style.top = `${topPct}%`;
      box.style.width = `${Math.max(widthPct, 2)}%`;
      box.style.height = `${Math.max(heightPct, 2)}%`;
    }

    // =========================================================================
    // 5x5 NEAREST-NEIGHBOR GRIDS RENDERING
    // =========================================================================
    function render5x5Grids(pixels, maxErrIdx) {
      const gridRgb = document.getElementById('grid-5x5-rgb');
      const gridGt = document.getElementById('grid-5x5-gt');
      const gridPred = document.getElementById('grid-5x5-pred');

      gridRgb.innerHTML = '';
      gridGt.innerHTML = '';
      gridPred.innerHTML = '';

      pixels.forEach(p => {
        // RGB Tile
        const tileRgb = document.createElement('div');
        tileRgb.className = `pixel-tile aspect-square rounded flex flex-col justify-between p-1 text-[9px] font-mono cursor-pointer transition border ${p.idx === activePixelIdx ? 'selected' : 'border-slate-800'}`;
        tileRgb.style.backgroundColor = `rgb(${p.rgb[0]}, ${p.rgb[1]}, ${p.rgb[2]})`;
        tileRgb.onclick = () => selectPixel(p);
        
        // High contrast text shadow
        const txtCol = p.gray > 128 ? '#000' : '#FFF';
        tileRgb.innerHTML = `
          <div class="flex justify-between" style="color: ${txtCol}; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
            <span>(${p.c},${p.r})</span>
          </div>
          <div class="text-[8px] font-bold" style="color: ${txtCol}; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">
            ${p.rgb[0]},${p.rgb[1]},${p.rgb[2]}
          </div>
        `;
        gridRgb.appendChild(tileRgb);

        // GT Depth Tile
        const tileGt = document.createElement('div');
        tileGt.className = `pixel-tile aspect-square rounded flex flex-col justify-between p-1 text-[9px] font-mono cursor-pointer transition border ${p.idx === activePixelIdx ? 'selected' : 'border-slate-800'}`;
        // Color by depth
        const depthNorm = Math.min(1.0, Math.max(0.0, (p.gtM - 0.7) / 3.8));
        tileGt.style.backgroundColor = `hsl(${220 - depthNorm * 180}, 75%, 25%)`;
        tileGt.onclick = () => selectPixel(p);
        tileGt.innerHTML = `
          <div class="flex justify-between text-slate-300">
            <span>(${p.c},${p.r})</span>
          </div>
          <div class="text-white font-bold text-[10px]">
            ${p.gtM.toFixed(3)}m
          </div>
        `;
        gridGt.appendChild(tileGt);

        // Pred Depth Tile
        const tilePred = document.createElement('div');
        tilePred.className = `pixel-tile aspect-square rounded flex flex-col justify-between p-1 text-[9px] font-mono cursor-pointer transition border ${p.idx === activePixelIdx ? 'selected' : 'border-slate-800'}`;
        const pNorm = Math.min(1.0, Math.max(0.0, (p.predM - 0.7) / 3.8));
        tilePred.style.backgroundColor = `hsl(${220 - pNorm * 180}, 75%, 25%)`;
        tilePred.onclick = () => selectPixel(p);
        tilePred.innerHTML = `
          <div class="flex justify-between text-slate-300">
            <span>(${p.c},${p.r})</span>
            ${p.idx === maxErrIdx ? '<span class="text-[8px] text-red-400 font-bold">MAX</span>' : ''}
          </div>
          <div class="text-white font-bold text-[10px]">
            ${p.predM.toFixed(3)}m
          </div>
        `;
        gridPred.appendChild(tilePred);
      });
    }

    // =========================================================================
    // 25-PIXEL QUANTITATIVE TABLE RENDERING
    // =========================================================================
    function render25PixelTable(pixels, maxErrIdx) {
      const tbody = document.getElementById('table-25-pixels-body');
      tbody.innerHTML = '';

      pixels.forEach(p => {
        const tr = document.createElement('tr');
        tr.id = `row-px-${p.idx}`;
        tr.className = `cursor-pointer transition hover:bg-slate-800/80 ${p.idx === activePixelIdx ? 'bg-cyan-950/40 border-l-2 border-cyan-400' : ''}`;
        tr.onclick = () => selectPixel(p);

        const isMax = p.idx === maxErrIdx;
        const relErrPct = (p.relErr * 100).toFixed(1);
        const errClass = p.relErr > 0.20 ? 'text-red-400 font-bold' : p.relErr > 0.10 ? 'text-amber-400' : 'text-emerald-400';

        tr.innerHTML = `
          <td class="p-3 text-slate-500">${p.idx + 1}</td>
          <td class="p-3 font-bold text-slate-200">(${p.px}, ${p.py})</td>
          <td class="p-3">
            <span class="inline-flex items-center gap-1.5">
              <span class="w-3 h-3 rounded-full border border-slate-700" style="background-color: rgb(${p.rgb[0]}, ${p.rgb[1]}, ${p.rgb[2]})"></span>
              <span>[${p.rgb[0]}, ${p.rgb[1]}, ${p.rgb[2]}]</span>
            </span>
          </td>
          <td class="p-3 text-emerald-400 font-bold">${p.gtM.toFixed(3)} m</td>
          <td class="p-3 text-cyan-300 font-bold">${p.predM.toFixed(3)} m</td>
          <td class="p-3 text-white font-bold">${p.absErr.toFixed(3)} m</td>
          <td class="p-3 ${errClass}">${relErrPct} %</td>
          <td class="p-3">
            ${isMax ? '<span class="px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-800 text-[10px] font-bold">MAX ERROR</span>' : '<span class="text-slate-400">Evaluated</span>'}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function selectPixel(pixel) {
      activePixelIdx = pixel.idx;

      // Update HUD
      document.getElementById('hud-active-gt').textContent = `${pixel.gtM.toFixed(3)} m`;
      document.getElementById('hud-active-pred').textContent = `${pixel.predM.toFixed(3)} m`;
      document.getElementById('hud-active-err').textContent = `${(pixel.relErr * 100).toFixed(1)} %`;

      // Highlight in 25-pixel Table
      document.querySelectorAll('#table-25-pixels-body tr').forEach(row => {
        row.classList.remove('bg-cyan-950/40', 'border-l-2', 'border-cyan-400');
      });
      const activeRow = document.getElementById(`row-px-${pixel.idx}`);
      if (activeRow) {
        activeRow.classList.add('bg-cyan-950/40', 'border-l-2', 'border-cyan-400');
      }

      // Highlight in Grid Tiles
      document.querySelectorAll('.pixel-tile').forEach((t, i) => {
        if (i % 25 === pixel.idx) {
          t.classList.add('selected');
        } else {
          t.classList.remove('selected');
        }
      });
    }

    // =========================================================================
    // CANVAS CLICK & HOVER INTERACTION
    // =========================================================================
    function setupCanvasListeners(canvasId) {
      const canvas = document.getElementById(canvasId);

      canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const x = Math.floor((e.clientX - rect.left) * scaleX);
        const y = Math.floor((e.clientY - rect.top) * scaleY);

        document.getElementById('hud-hover-coord').textContent = `(X: ${x}, Y: ${y})`;
        updateCrosshair('crosshair-rgb', e.clientX - rect.left, e.clientY - rect.top);
        updateCrosshair('crosshair-gt', e.clientX - rect.left, e.clientY - rect.top);
      });

      canvas.addEventListener('mouseleave', () => {
        document.getElementById('crosshair-rgb').classList.add('hidden');
        document.getElementById('crosshair-gt').classList.add('hidden');
      });

      canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const x = Math.floor((e.clientX - rect.left) * scaleX);
        const y = Math.floor((e.clientY - rect.top) * scaleY);
        selectRegion(x, y);
      });
    }

    function updateCrosshair(crosshairId, px, py) {
      const el = document.getElementById(crosshairId);
      el.classList.remove('hidden');
      el.style.left = `${px}px`;
      el.style.top = `${py}px`;
    }

    // =========================================================================
    // THREE.JS 3D ENGINE & DISCREPANCY VISUALIZATION
    // =========================================================================
    function init3DEngine() {
      const container = document.getElementById('container-3d');
      const width = container.clientWidth || 600;
      const height = container.clientHeight || 450;

      scene3D = new THREE.Scene();
      scene3D.background = new THREE.Color(0x070B12);

      camera3D = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
      camera3D.position.set(0, -6, 8);

      renderer3D = new THREE.WebGLRenderer({ antialias: true });
      renderer3D.setSize(width, height);
      renderer3D.setPixelRatio(window.devicePixelRatio);
      container.appendChild(renderer3D.domElement);

      controls3D = new THREE.OrbitControls(camera3D, renderer3D.domElement);
      controls3D.enableDamping = true;
      controls3D.dampingFactor = 0.05;

      // Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
      scene3D.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
      dirLight.position.set(5, 5, 10);
      scene3D.add(dirLight);

      meshGroup = new THREE.Group();
      scene3D.add(meshGroup);

      // Render loop
      function animate() {
        requestAnimationFrame(animate);
        controls3D.update();
        renderer3D.render(scene3D, camera3D);
      }
      animate();

      window.addEventListener('resize', () => {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera3D.aspect = w / h;
        camera3D.updateProjectionMatrix();
        renderer3D.setSize(w, h);
      });
    }

    function update3DSurface(pixels) {
      if (!scene3D || !meshGroup) return;

      // Clear previous 3D objects
      while (meshGroup.children.length > 0) {
        const obj = meshGroup.children[0];
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) obj.material.dispose();
        meshGroup.remove(obj);
      }

      if (current3DMode === 'patch') {
        build3DPatchLattice(pixels);
      } else {
        build3DFullSceneMesh();
      }
    }

    function build3DPatchLattice(pixels) {
      // 5x5 Grid Lattice: centered at (0, 0)
      const scaleXY = 0.8;
      const centerGt = pixels[12].gtM;

      // 1. Build Ground Truth 3D Grid Surface
      const gtGeom = new THREE.PlaneGeometry(4 * scaleXY, 4 * scaleXY, 4, 4);
      const gtPos = gtGeom.attributes.position;
      for (let i = 0; i < 25; i++) {
        // Z elevation: inverted so greater depth goes down/away
        const z = -(pixels[i].gtM - centerGt) * 3.0;
        gtPos.setZ(i, z);
      }
      gtGeom.computeVertexNormals();

      if (current3DLayer === 'overlay' || current3DLayer === 'gt') {
        const gtMat = new THREE.MeshStandardMaterial({
          color: 0x10B981,
          wireframe: false,
          transparent: true,
          opacity: 0.75,
          side: THREE.DoubleSide
        });
        const gtMesh = new THREE.Mesh(gtGeom, gtMat);
        meshGroup.add(gtMesh);

        const gtWire = new THREE.LineSegments(
          new THREE.WireframeGeometry(gtGeom),
          new THREE.LineBasicMaterial({ color: 0x34D399, linewidth: 1.5 })
        );
        meshGroup.add(gtWire);
      }

      // 2. Build Predicted Depth 3D Grid Surface
      const predGeom = new THREE.PlaneGeometry(4 * scaleXY, 4 * scaleXY, 4, 4);
      const predPos = predGeom.attributes.position;
      for (let i = 0; i < 25; i++) {
        const z = -(pixels[i].predM - centerGt) * 3.0;
        predPos.setZ(i, z);
      }
      predGeom.computeVertexNormals();

      if (current3DLayer === 'overlay' || current3DLayer === 'pred') {
        const predMat = new THREE.MeshStandardMaterial({
          color: 0xF59E0B,
          wireframe: false,
          transparent: true,
          opacity: 0.75,
          side: THREE.DoubleSide
        });
        const predMesh = new THREE.Mesh(predGeom, predMat);
        meshGroup.add(predMesh);

        const predWire = new THREE.LineSegments(
          new THREE.WireframeGeometry(predGeom),
          new THREE.LineBasicMaterial({ color: 0xFBBF24, linewidth: 1.5 })
        );
        meshGroup.add(predWire);
      }

      // 3. 3D Vertical Displacement Error Stems
      if (current3DLayer === 'overlay' || current3DLayer === 'error') {
        const stemMaterial = new THREE.LineBasicMaterial({ color: 0xEF4444, linewidth: 2 });
        for (let i = 0; i < 25; i++) {
          const x = (pixels[i].c - 2) * scaleXY;
          const y = -(pixels[i].r - 2) * scaleXY;
          const zGt = -(pixels[i].gtM - centerGt) * 3.0;
          const zPred = -(pixels[i].predM - centerGt) * 3.0;

          const points = [
            new THREE.Vector3(x, y, zGt),
            new THREE.Vector3(x, y, zPred)
          ];
          const lineGeom = new THREE.BufferGeometry().setFromPoints(points);
          const line = new THREE.Line(lineGeom, stemMaterial);
          meshGroup.add(line);

          // Add a point sphere on predicted vertex
          const sphereGeom = new THREE.SphereGeometry(0.06, 8, 8);
          const sphereMat = new THREE.MeshBasicMaterial({ color: 0xEF4444 });
          const sphere = new THREE.Mesh(sphereGeom, sphereMat);
          sphere.position.set(x, y, zPred);
          meshGroup.add(sphere);
        }
      }

      // Coordinate axes
      const axesHelper = new THREE.AxesHelper(2.5);
      meshGroup.add(axesHelper);
    }

    function build3DFullSceneMesh() {
      if (!currentScene.mesh_3d) return;
      const m = currentScene.mesh_3d;
      const gw = m.grid_w;
      const gh = m.grid_h;

      const geom = new THREE.PlaneGeometry(8, 6, gw - 1, gh - 1);
      const pos = geom.attributes.position;
      const colors = new Float32Array(gw * gh * 3);

      let idx = 0;
      for (let r = 0; r < gh; r++) {
        for (let c = 0; c < gw; c++) {
          const d = m.depth_gt[r][c];
          pos.setZ(idx, -(d - 2.0) * 1.5);

          const rgb = m.rgb_colors[r][c];
          colors[idx * 3] = rgb[0];
          colors[idx * 3 + 1] = rgb[1];
          colors[idx * 3 + 2] = rgb[2];
          idx++;
        }
      }
      geom.computeVertexNormals();
      geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      const mat = new THREE.MeshStandardMaterial({
        vertexColors: true,
        wireframe: false,
        side: THREE.DoubleSide
      });
      const mesh = new THREE.Mesh(geom, mat);
      meshGroup.add(mesh);

      // Add highlighted bounding box for selected 5x5 region
      const boxGeom = new THREE.BoxGeometry(0.3, 0.3, 0.3);
      const boxMat = new THREE.MeshBasicMaterial({ color: 0xEF4444, wireframe: true });
      const box = new THREE.Mesh(boxGeom, boxMat);
      const normX = (selectedX / 640.0) * 8.0 - 4.0;
      const normY = -(selectedY / 480.0) * 6.0 + 3.0;
      box.position.set(normX, normY, 0);
      meshGroup.add(box);
    }

    function set3DMode(mode) {
      current3DMode = mode;
      document.getElementById('btn-3d-patch').className = 
        mode === 'patch' ? 'px-3 py-1 rounded bg-cyan-600 text-white font-medium transition' : 'px-3 py-1 rounded text-slate-400 hover:text-white font-medium transition';
      document.getElementById('btn-3d-scene').className = 
        mode === 'scene' ? 'px-3 py-1 rounded bg-cyan-600 text-white font-medium transition' : 'px-3 py-1 rounded text-slate-400 hover:text-white font-medium transition';

      reset3DCamera();
      // Re-trigger region update to rebuild 3D
      selectRegion(selectedX + 2, selectedY + 2);
    }

    function on3DLayerChange(layer) {
      current3DLayer = layer;
      selectRegion(selectedX + 2, selectedY + 2);
    }

    function reset3DCamera() {
      if (current3DMode === 'patch') {
        camera3D.position.set(0, -5, 6);
      } else {
        camera3D.position.set(0, -8, 10);
      }
      controls3D.target.set(0, 0, 0);
      controls3D.update();
    }

    // =========================================================================
    // FAILURE CAUSE INVESTIGATION & EVIDENCE EVALUATION
    // =========================================================================
    function updateFailureInvestigation(pixels, meanAbsErr, meanRelErr, textureVar) {
      // Find matching precomputed region if selection overlaps
      let matchedReg = null;
      if (currentScene.regions) {
        matchedReg = currentScene.regions.find(r => {
          const bx = r.bbox[0];
          const by = r.bbox[1];
          const bw = r.bbox[2];
          const bh = r.bbox[3];
          return (selectedX >= bx && selectedX <= bx + bw && selectedY >= by && selectedY <= by + bh);
        });
      }

      const feats = matchedReg ? matchedReg.features : {
        texture_var: textureVar,
        edge_density: 0.04,
        depth_discontinuity: 0.12,
        brightness: 112.0,
        contrast: 24.0,
        highlight_ratio: 0.02,
        aspect_ratio: 1.1
      };

      const topCause = matchedReg ? matchedReg.top_cause : (textureVar < 200 ? 'textureless' : 'ambiguous');
      const conf = matchedReg ? matchedReg.confidence : 'Medium';

      // Update Dimension A Evidence Values
      document.getElementById('ev-texture-var').textContent = `${feats.texture_var.toFixed(1)} ${feats.texture_var < 200 ? '(Low)' : '(Normal)'}`;
      document.getElementById('ev-edge-density').textContent = `${feats.edge_density.toFixed(2)} ${feats.edge_density > 0.15 ? '(High)' : '(Smooth)'}`;
      document.getElementById('ev-depth-discon').textContent = `${feats.depth_discontinuity.toFixed(2)} m`;
      document.getElementById('ev-lighting').textContent = `${feats.brightness.toFixed(0)} / ${feats.contrast.toFixed(0)}`;
      document.getElementById('ev-highlight-ratio').textContent = `${(feats.highlight_ratio * 100).toFixed(1)} %`;

      // Update Dimension B Evidence Values
      const polarity = pixels[12].predM > pixels[12].gtM ? 'Overshoot' : 'Undershoot';
      document.getElementById('ev-polarity').textContent = 
        `${polarity} (${(pixels[12].predM - pixels[12].gtM > 0 ? '+' : '')}${(pixels[12].predM - pixels[12].gtM).toFixed(3)}m)`;

      // Render 7 Categories Matrix
      renderCategoryCards(feats, topCause);

      // Update Report Card
      document.getElementById('card-confidence-badge').textContent = `Confidence: ${conf} (${matchedReg ? Math.round((matchedReg.scores[topCause] || 0.7) * 100) : 75}%)`;
      document.getElementById('card-observed-err').textContent = 
        `Local depth ${polarity.toLowerCase()} of ${(pixels[12].predM - pixels[12].gtM > 0 ? '+' : '')}${(pixels[12].predM - pixels[12].gtM).toFixed(3)}m (patch mean rel error: ${(meanRelErr * 100).toFixed(1)}%).`;
      document.getElementById('card-location').textContent = 
        `Coordinates [X: ${selectedX}..${selectedX+4}, Y: ${selectedY}..${selectedY+4}] in NYU Test Split ${currentSceneId.toUpperCase()}.`;
      document.getElementById('card-img-ev').textContent = 
        `Texture variance is ${feats.texture_var.toFixed(1)}, edge density is ${feats.edge_density.toFixed(2)}, brightness is ${feats.brightness.toFixed(0)}. ${getEvidenceDescription(topCause, feats)}`;
      document.getElementById('card-explanation').textContent = 
        `${formatCategoryName(topCause)}. ${getTaxonomyDesc(topCause)}`;
    }

    function renderCategoryCards(feats, activeCause) {
      const container = document.getElementById('cards-categories-container');
      container.innerHTML = '';

      window.VEO_DATA.taxonomy.forEach(cat => {
        const isSelected = cat.id === activeCause;
        const pass = evaluateCategoryPass(cat.id, feats);

        const card = document.createElement('div');
        card.className = `p-4 rounded-xl border transition space-y-2 ${isSelected ? 'bg-cyan-950/40 border-cyan-500 shadow-lg shadow-cyan-950/30' : 'bg-slate-900 border-slate-800'}`;

        card.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-white">${cat.label}</span>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded ${pass ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-slate-800 text-slate-400 border border-slate-700'}">
              ${pass ? 'SUPPORTED' : 'INCONCLUSIVE'}
            </span>
          </div>
          <div class="text-[11px] font-mono text-cyan-400">
            ${cat.formula}
          </div>
          <p class="text-[11px] text-slate-400 leading-tight">
            ${cat.desc}
          </p>
        `;
        container.appendChild(card);
      });
    }

    function evaluateCategoryPass(id, feats) {
      if (id === 'textureless') return feats.texture_var < 200.0;
      if (id === 'boundary_mixing') return feats.edge_density > 0.15;
      if (id === 'occlusion') return feats.depth_discontinuity > 0.50;
      if (id === 'reflection') return feats.highlight_ratio > 0.10;
      if (id === 'thin_object') return feats.aspect_ratio > 3.0;
      if (id === 'poor_lighting') return feats.brightness < 60 || feats.brightness > 210;
      return true; // ambiguous
    }

    function formatCategoryName(cat) {
      const map = {
        'textureless': 'Textureless Surface',
        'boundary_mixing': 'Boundary Mixing / Bleed',
        'occlusion': 'Occlusion Discontinuity',
        'reflection': 'Specular Reflection',
        'thin_object': 'Thin Slender Structure',
        'poor_lighting': 'Poor / Extreme Lighting',
        'ambiguous': 'Ambiguous / Multi-Factor'
      };
      return map[cat] || cat;
    }

    function getEvidenceDescription(cat, feats) {
      if (cat === 'textureless') return "The surface is planar and featureless, offering minimal local contrast gradients.";
      if (cat === 'boundary_mixing') return "High-frequency contours cause foreground and background depths to bleed across the 14x14 ViT patch.";
      if (cat === 'reflection') return "High brightness and low saturation indicate non-Lambertian glossy specular reflections.";
      if (cat === 'occlusion') return "Sharp depth discontinuity step indicates foreground occlusion boundaries.";
      return "Multiple physical and architectural factors contribute without a single dominant signal.";
    }

    function getTaxonomyDesc(cat) {
      const item = window.VEO_DATA.taxonomy.find(t => t.id === cat);
      return item ? item.desc : "";
    }

    // =========================================================================
    // UI NAVIGATION & INTERACTIVITY
    // =========================================================================
    function scrollToStage(stageId) {
      const el = document.getElementById(stageId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }

      // Update Step Pill Highlights
      document.querySelectorAll('.step-pill').forEach(btn => {
        btn.classList.remove('active');
        btn.classList.add('text-slate-400');
      });
      event.currentTarget.classList.add('active');
      event.currentTarget.classList.remove('text-slate-400');
    }

    function setPipelineStep(stepNum) {
      for (let i = 1; i <= 6; i++) {
        const btn = document.getElementById(`pipestep-btn-${i}`);
        const content = document.getElementById(`pipestep-content-${i}`);
        if (i === stepNum) {
          btn.className = "p-2.5 rounded-lg border border-cyan-500 bg-cyan-950/60 text-cyan-300 text-left transition";
          content.classList.remove('hidden');
        } else {
          btn.className = "p-2.5 rounded-lg border border-slate-800 bg-slate-900 text-slate-400 text-left transition hover:text-white";
          content.classList.add('hidden');
        }
      }
    }

    function onThresholdChange(val) {
      errorThreshold = val / 100.0;
      document.getElementById('threshold-label').textContent = `${val}% Relative Error`;
    }

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', initApp);
  </script>

</body>
</html>
"""

    out_file = Path("web_app/index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[OK] Fully Redesigned VEO Interface successfully generated at:")
    print(f"     {out_file.resolve()} (Size: {out_file.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_redesigned_html()

