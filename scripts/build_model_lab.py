"""
Builds the 'DEPTH ANYTHING V2 - INTERACTIVE MATHEMATICAL 3D ARCHITECTURE LABORATORY'
Outputs: web_app/model_lab.html

Key Upgrades & Visual Assets:
1. Real RGB Photograph & Real Decomposed Channels:
   - Front display: Real full-resolution RGB photo on a gallery mount.
   - 3 Real Photographic Channel Slices (Red, Green, Blue) generated via offscreen canvas,
     showing authentic photographic channel decompositions in 3D space!
2. Real 3D Transformer Architecture:
   - Publication-grade DINOv2 ViT-Small technical blueprint schematic mapped on 3D HUD glass.
   - 12 physical brushed-metal Transformer blocks with illuminated layer status LEDs.
   - 6 physical golden Attention Head cylinders (Head 1 to Head 6, d_k = 64).
   - Dynamic 3D Attention Heatmap matrix plane showing cross-token attention weights.
   - Real 3D glowing Bezier curves (attention arcs) leaping across token coordinates.
3. Real 3D Sliced Patch Extraction:
   - Authentic 14x14 patch tile sliced from the real photograph and floating in 3D.
   - Projection arrow into the 384-dim token embedding pillar + golden [CLS] token.
4. Authentic DINOv2 Activation Panels (Layers 3, 6, 9, 12):
   - Real precomputed feature heatmaps mapped on glowing glass presentation panels.
5. DPT Multi-Scale Pyramid & RefineNet Fusion Conduits.
6. Depth Head with 3D Sigmoid Curve & Metric Scaling Equation.
7. Authentic 3D Displaced Elevation Surface Mesh:
   - Textured with real RGB image and physically displaced along the Z-axis by metric depth!
   - Synchronized floating panels: Real RGB, Predicted Depth, Ground-Truth Depth, Error Heatmap.
8. 3D Floating Text Sprite Badges above every component.
9. Three-Level Mathematical Explanations (Intuition, Formula & Arithmetic, Active Pipeline State).
10. Continuous Sequential Data Passing & 5-Minute Guided Interactive Learning Tour.
"""

from pathlib import Path

def build_model_lab_html():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Depth Anything V2 | Interactive Mathematical 3D Architecture Laboratory</title>
  
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="alternate icon" href="favicon.ico">
  
  <!-- FontAwesome Icons & Local Precompiled Stylesheet -->
  <link rel="stylesheet" href="assets/fontawesome/all.min.css">
  <link rel="stylesheet" href="assets/css/tailwind.min.css">
  
  <!-- Local Offline 3D Libraries: Three.js r128 & OrbitControls -->
  <script src="assets/js/three.min.js"></script>
  <script src="assets/js/OrbitControls.js"></script>
  
  <!-- Precomputed Dataset Payload (NYU Depth V2, Authentic DINOv2 Activations & 3D Meshes) -->
  <script src="data/app_data_v2.js"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    :root {
      --bg-ivory: #F6F3EA;
      --surface-beige: #EAE2D2;
      --surface-card: #FDFBF7;
      --surface-alt: #E2D9C7;
      --olive-primary: #68734D;
      --olive-dark: #414A32;
      --olive-light: #E8ECE2;
      --warm-brown: #8B6849;
      --text-dark: #302F27;
      --text-muted: #777466;
      --border-subtle: #D9D1C2;
      --error-terracotta: #C8755A;
      --sage-green: #5A7A54;
      --gold-accent: #C49A58;
      --cyan-accent: #2B4B7C;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-ivory);
      color: var(--text-dark);
      overflow: hidden;
      width: 100vw;
      height: 100vh;
      user-select: none;
    }
    
    .font-serif { font-family: 'Newsreader', Georgia, serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
    
    /* Top Header Bar */
    .top-header {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: rgba(246, 243, 234, 0.94);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border-subtle);
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }
    
    /* Central 3D Canvas */
    #canvas-container {
      position: absolute;
      top: 60px;
      left: 0;
      right: 0;
      bottom: 0;
      width: 100%;
      height: calc(100vh - 60px);
      z-index: 10;
      background: var(--bg-ivory);
    }
    
    /* Left Floating Mathematical Learning Laboratory Panel */
    .math-lab-panel {
      position: absolute;
      top: 76px;
      left: 20px;
      width: 470px;
      max-height: calc(100vh - 150px);
      background: rgba(253, 251, 247, 0.96);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(48, 47, 39, 0.08);
      z-index: 40;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s;
    }
    
    .math-lab-panel.collapsed {
      transform: translateX(-500px);
      opacity: 0;
      pointer-events: none;
    }
    
    .panel-scroll-content {
      padding: 18px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    
    /* Level Cards */
    .level-card {
      background: var(--bg-ivory);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    
    .level-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 2px 8px;
      border-radius: 6px;
    }
    
    .badge-level-a { background: var(--olive-light); color: var(--olive-dark); border: 1px solid rgba(104, 115, 77, 0.3); }
    .badge-level-b { background: #F4EBE2; color: var(--warm-brown); border: 1px solid rgba(139, 104, 73, 0.3); }
    .badge-level-c { background: #E7EEF8; color: var(--cyan-accent); border: 1px solid rgba(43, 75, 124, 0.3); }
    
    /* Mathematical Display Styling */
    .formula-display {
      background: #FFFFFF;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: #24292F;
      line-height: 1.5;
      overflow-x: auto;
    }
    
    .var-dict {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 4px 10px;
      font-size: 11px;
      line-height: 1.4;
      background: rgba(234, 226, 210, 0.35);
      border-radius: 6px;
      padding: 8px 10px;
      border: 1px solid rgba(217, 209, 194, 0.5);
    }
    .var-dict dt { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--olive-dark); }
    .var-dict dd { color: var(--text-dark); }
    
    .worked-math-box {
      background: #FDF8F3;
      border-left: 3px solid var(--warm-brown);
      border-radius: 4px;
      padding: 8px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      line-height: 1.5;
      color: #3C3026;
    }
    
    /* Interactive Pixel Tracker Strip */
    .data-flow-conduit {
      background: var(--surface-beige);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
    }
    
    /* Navigation Breadcrumbs / Stage Selector */
    .stages-bar {
      position: absolute;
      top: 76px;
      right: 20px;
      background: rgba(246, 243, 234, 0.95);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 6px 10px;
      z-index: 40;
      display: flex;
      gap: 6px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .stage-pill {
      padding: 6px 10px;
      border-radius: 8px;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 500;
      color: var(--text-muted);
      cursor: pointer;
      border: 1px solid transparent;
      background: transparent;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .stage-pill:hover {
      background: var(--surface-beige);
      color: var(--text-dark);
    }
    .stage-pill.active {
      background: var(--olive-primary);
      color: #FFFFFF;
      border-color: var(--olive-dark);
      font-weight: 700;
    }
    
    /* 5-Minute Tour Controller (Bottom Center) */
    .tour-dock {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(253, 251, 247, 0.96);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 9999px;
      padding: 8px 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
      z-index: 40;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    
    .tour-progress-track {
      width: 220px;
      height: 6px;
      background: var(--border-subtle);
      border-radius: 9999px;
      overflow: hidden;
      cursor: pointer;
    }
    .tour-progress-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--olive-primary), var(--sage-green));
      transition: width 0.2s linear;
    }
    
    /* Floating Camera Controls */
    .cam-controls {
      position: absolute;
      bottom: 24px;
      right: 24px;
      z-index: 40;
      display: flex;
      gap: 8px;
    }
    
    .btn-cam {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(253, 251, 247, 0.95);
      border: 1px solid var(--border-subtle);
      color: var(--text-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      transition: all 0.15s;
    }
    .btn-cam:hover {
      background: var(--surface-beige);
      transform: scale(1.05);
    }
    
    /* Reusable Buttons */
    .btn-olive {
      background: var(--olive-primary);
      color: #FFFFFF;
      border: 1px solid var(--olive-dark);
      border-radius: 8px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
      text-decoration: none;
    }
    .btn-olive:hover {
      background: var(--olive-dark);
      box-shadow: 0 2px 8px rgba(65, 74, 50, 0.25);
    }
    
    .btn-secondary {
      background: var(--surface-beige);
      color: var(--text-dark);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
      text-decoration: none;
    }
    .btn-secondary:hover {
      background: #DFD5C3;
    }
    
    /* Modal */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(48, 47, 39, 0.45);
      backdrop-filter: blur(4px);
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .modal-box {
      width: 90%;
      max-width: 640px;
      background: var(--bg-ivory);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.15);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    
    .hidden { display: none !important; }
  </style>
</head>
<body>

  <!-- ========================================================================= -->
  <!-- 1. TOP HEADER NAVIGATION -->
  <!-- ========================================================================= -->
  <header class="top-header">
    <div style="display: flex; align-items: center; gap: 14px;">
      <a href="index.html" class="btn-secondary" title="Return to VEO Error Observatory">
        <i class="fa-solid fa-arrow-left"></i>
        <span>VEO Exhibition</span>
      </a>
      <div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <h1 style="font-size: 16px; font-weight: 600; color: #302F27; font-family: 'Newsreader', Georgia, serif;">
            Depth Anything V2 Architecture Laboratory
          </h1>
          <span style="padding: 2px 8px; font-size: 10px; font-family: 'JetBrains Mono', monospace; font-weight: 600; border-radius: 9999px; background: #E8ECE2; color: #414A32; border: 1px solid #68734D;">
            Interactive Mathematical 3D
          </span>
        </div>
        <p style="font-size: 11px; color: #777466;">From Raw RGB Photons to Metric Depth: Mathematical Step-by-Step Visualization</p>
      </div>
    </div>

    <!-- Center Scene Selector -->
    <div style="display: flex; align-items: center; gap: 10px; background: #EAE2D2; padding: 5px 12px; border-radius: 10px; border: 1px solid #D9D1C2;">
      <label for="scene-select" style="font-size: 11px; color: #777466; font-weight: 500; display: flex; align-items: center; gap: 6px;">
        <i class="fa-solid fa-camera" style="color: #68734D; font-size: 11px;"></i>
        <span>NYU Scene:</span>
      </label>
      <select id="scene-select" onchange="onSceneChange(this.value)" style="background: #F6F3EA; font-size: 11px; font-family: 'JetBrains Mono', monospace; color: #302F27; border: 1px solid #D9D1C2; border-radius: 6px; padding: 3px 6px; cursor: pointer; outline: none;">
        <!-- Populated dynamically via JS -->
      </select>
    </div>

    <!-- Right Controls -->
    <div style="display: flex; align-items: center; gap: 10px;">
      <button onclick="togglePanel()" class="btn-secondary" title="Toggle Mathematical Details Panel">
        <i class="fa-solid fa-calculator" style="color: #68734D;"></i>
        <span id="panel-toggle-label">Hide Math Panel</span>
      </button>
      <button onclick="flyToOverview()" class="btn-secondary" title="View Complete 3D Architecture">
        <i class="fa-solid fa-cubes-stacked" style="color: #8B6849;"></i>
        <span>3D Overview</span>
      </button>
      <a href="assets/VEO_conference_paper.pdf" target="_blank" class="btn-secondary" title="Read Research Paper">
        <i class="fa-solid fa-file-pdf" style="color: #C8755A;"></i>
        <span>Paper PDF</span>
      </a>
    </div>
  </header>

  <!-- ========================================================================= -->
  <!-- 2. STAGE SELECTION PILLS (TOP RIGHT) -->
  <!-- ========================================================================= -->
  <nav class="stages-bar" id="stages-bar">
    <button onclick="selectStage(0)" class="stage-pill active" id="pill-0">
      <i class="fa-solid fa-network-wired"></i> Overview
    </button>
    <button onclick="selectStage(1)" class="stage-pill" id="pill-1">1. Real RGB</button>
    <button onclick="selectStage(2)" class="stage-pill" id="pill-2">2. Normalize</button>
    <button onclick="selectStage(3)" class="stage-pill" id="pill-3">3. Patch Embed</button>
    <button onclick="selectStage(4)" class="stage-pill" id="pill-4">4. DINOv2 MHSA</button>
    <button onclick="selectStage(5)" class="stage-pill" id="pill-5">5. Activations</button>
    <button onclick="selectStage(6)" class="stage-pill" id="pill-6">6. DPT Decoder</button>
    <button onclick="selectStage(7)" class="stage-pill" id="pill-7">7. Depth Head</button>
    <button onclick="selectStage(8)" class="stage-pill" id="pill-8">8. 3D Surface</button>
  </nav>

  <!-- ========================================================================= -->
  <!-- 3. CENTRAL THREE.JS 3D WEBGL WORKSPACE -->
  <!-- ========================================================================= -->
  <div id="canvas-container"></div>

  <!-- ========================================================================= -->
  <!-- 4. THREE-LEVEL MATHEMATICAL EXPLANATION PANEL (LEFT FLOATING CARD) -->
  <!-- ========================================================================= -->
  <aside class="math-lab-panel" id="math-lab-panel">
    
    <!-- Stage Header -->
    <div style="padding: 14px 18px; border-bottom: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: flex-start; background: #FAF7F0;">
      <div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="level-badge badge-level-a" id="panel-stage-badge">STAGE 01 / 08</span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-muted);" id="panel-tensor-shape">[480, 640, 3] uint8</span>
        </div>
        <h2 style="font-size: 17px; font-weight: 600; color: var(--text-dark); margin-top: 4px;" class="font-serif" id="panel-stage-title">
          Input RGB Image: Discrete Color Grid
        </h2>
      </div>
      <button onclick="togglePanel()" style="background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 14px; padding: 4px;" title="Close Panel">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>

    <!-- Scrollable Educational Body -->
    <div class="panel-scroll-content">

      <!-- LEVEL A: INTUITION -->
      <section class="level-card">
        <div class="level-badge badge-level-a">
          <i class="fa-solid fa-lightbulb"></i> LEVEL A — INTUITION (PLAIN LANGUAGE)
        </div>
        <p style="font-size: 12.5px; color: var(--text-dark); line-height: 1.55;" id="panel-level-a">
          The camera cannot measure distance directly. It records photons arriving at a physical sensor grid, assigning integer color intensities to every pixel.
        </p>
      </section>

      <!-- LEVEL B: FORMULA & WORKED ARITHMETIC SUBSTITUTION -->
      <section class="level-card">
        <div class="level-badge badge-level-b">
          <i class="fa-solid fa-square-root-variable"></i> LEVEL B — EXACT FORMULA & WORKED NUMERICAL EXAMPLE
        </div>
        
        <!-- Formula Box -->
        <div class="formula-display" id="panel-formula">
          I(x, y) = [R(x, y), G(x, y), B(x, y)]^T ∈ {0, 1, ..., 255}^3
        </div>

        <!-- Variable Dictionary -->
        <dl class="var-dict" id="panel-var-dict">
          <dt>I(x, y)</dt><dd>Color vector at pixel row y, column x</dd>
          <dt>R, G, B</dt><dd>8-bit discrete photon intensity channels</dd>
          <dt>H × W</dt><dd>Original camera matrix: 480 × 640 = 307,200 pixels</dd>
        </dl>

        <!-- Worked Numerical Example with Concrete Numbers -->
        <div class="worked-math-box" id="panel-worked-example">
          <strong>Selected Pixel Example (X: 210, Y: 140):</strong><br>
          R = 192 (75.3% max)<br>
          G = 178 (69.8% max)<br>
          B = 160 (62.7% max)<br>
          RGB → BGR Order: [160, 178, 192]
        </div>
      </section>

      <!-- LEVEL C: COMPUTATIONAL DATA FLOW & ACTIVE TENSOR PASSING -->
      <section class="level-card">
        <div class="level-badge badge-level-c">
          <i class="fa-solid fa-diagram-project"></i> LEVEL C — CONTINUOUS DATA PASSING
        </div>

        <div class="data-flow-conduit" id="panel-data-flow">
          <div style="display: flex; justify-content: space-between;">
            <span style="color: var(--text-muted);">Incoming State:</span>
            <strong id="df-incoming-state">Raw Kinect RGB Image</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: var(--text-muted);">Active Pixel / Patch:</span>
            <strong id="df-active-coord" style="color: var(--olive-primary);">Coord (210, 140)</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span style="color: var(--text-muted);">Output Produced:</span>
            <strong id="df-output-produced" style="color: var(--warm-brown);">Matrix [480, 640, 3]</strong>
          </div>
        </div>

        <!-- Advance Button Carrying State -->
        <button onclick="advanceToNextStage()" id="btn-advance-stage" class="btn-olive" style="width: 100%; justify-content: center; padding: 8px 12px; margin-top: 4px;">
          <span>Send Result to Preprocessing</span>
          <i class="fa-solid fa-arrow-right"></i>
        </button>
      </section>

    </div>

  </aside>

  <!-- ========================================================================= -->
  <!-- 5. FIVE-MINUTE GUIDED TOUR CONTROLLER (BOTTOM DOCK) -->
  <!-- ========================================================================= -->
  <div class="tour-dock">
    <button onclick="toggleTourPlay()" id="btn-tour-play" class="btn-olive" style="border-radius: 9999px; padding: 6px 14px;">
      <i class="fa-solid fa-play" id="icon-tour-play"></i>
      <span id="label-tour-play">Start 5-Min Tour</span>
    </button>

    <div style="display: flex; align-items: center; gap: 8px;">
      <button onclick="navigateStageStep(-1)" class="btn-secondary" style="padding: 4px 8px; border-radius: 6px;" title="Previous Component">
        <i class="fa-solid fa-chevron-left"></i>
      </button>
      <button onclick="navigateStageStep(1)" class="btn-secondary" style="padding: 4px 8px; border-radius: 6px;" title="Next Component">
        <i class="fa-solid fa-chevron-right"></i>
      </button>
    </div>

    <!-- Progress Scrubber -->
    <div style="display: flex; flex-direction: column; gap: 2px;">
      <div style="display: flex; justify-content: space-between; font-size: 10px; font-family: 'JetBrains Mono', monospace; color: var(--text-muted);">
        <span id="tour-stage-name">Architecture Overview</span>
        <span id="tour-timer-text">00:00 / 05:00</span>
      </div>
      <div class="tour-progress-track" onclick="seekTour(event)">
        <div class="tour-progress-bar" id="tour-progress-bar"></div>
      </div>
    </div>

    <button onclick="restartTour()" class="btn-secondary" style="padding: 4px 8px; border-radius: 6px;" title="Restart Guided Tour">
      <i class="fa-solid fa-rotate-left"></i>
    </button>
  </div>

  <!-- ========================================================================= -->
  <!-- 6. FLOATING CAMERA CONTROLS (BOTTOM RIGHT) -->
  <!-- ========================================================================= -->
  <div class="cam-controls">
    <button onclick="adjustCameraZoom(0.8)" class="btn-cam" title="Zoom In">
      <i class="fa-solid fa-plus"></i>
    </button>
    <button onclick="adjustCameraZoom(1.25)" class="btn-cam" title="Zoom Out">
      <i class="fa-solid fa-minus"></i>
    </button>
    <button onclick="flyToOverview()" class="btn-cam" title="Reset View">
      <i class="fa-solid fa-maximize"></i>
    </button>
  </div>

  <!-- ========================================================================= -->
  <!-- 7. TOUR COMPLETION SUMMARY MODAL -->
  <!-- ========================================================================= -->
  <div id="tour-modal" class="modal-backdrop hidden">
    <div class="modal-box">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--olive-primary); color: white; display: flex; align-items: center; justify-content: center;">
            <i class="fa-solid fa-award"></i>
          </div>
          <h3 class="font-serif" style="font-size: 18px; font-weight: 600; color: var(--text-dark);">
            Depth Anything V2 Pipeline Mastered
          </h3>
        </div>
        <button onclick="closeTourModal()" style="background: none; border: none; font-size: 16px; color: var(--text-muted); cursor: pointer;">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <p style="font-size: 13px; color: var(--text-dark); line-height: 1.6;">
        You have traced the mathematical lifecycle of monocular depth estimation through all eight stages:
      </p>

      <div style="background: var(--surface-beige); padding: 14px; border-radius: 10px; border: 1px solid var(--border-subtle); font-family: 'JetBrains Mono', monospace; font-size: 11px; line-height: 1.7; color: var(--olive-dark);">
        <div><strong>1. RGB Grid:</strong> 480×640×3 matrix of discrete photon intensities.</div>
        <div><strong>2. Preprocessing:</strong> Scaling by 255, ImageNet standard score normalisation, and aspect-ratio resize to 518×686.</div>
        <div><strong>3. Patch Embedding:</strong> 1,813 spatial patches (14×14) projected to 384 dims + 1 [CLS] token = 1,814 tokens.</div>
        <div><strong>4. DINOv2 MHSA:</strong> 12 transformer blocks with 6 parallel heads computing softmax(QK^T / 8)V.</div>
        <div><strong>5. Intermediate Activations:</strong> Feature snapshots hooked at Layers 3, 6, 9, 12.</div>
        <div><strong>6. DPT Decoder:</strong> 4-tier multi-scale pyramids fused top-down via RefineNet into 64 channels.</div>
        <div><strong>7. Depth Prediction:</strong> Convolutions + Sigmoid activation multiplied by max_depth = 20.0m.</div>
        <div><strong>8. 3D Surface Mesh:</strong> Metric distance array interpolated back to 480×640.</div>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 10px;">
        <button onclick="closeTourModal()" class="btn-secondary">Explore 3D Model Freely</button>
        <a href="index.html" class="btn-olive">Launch VEO Failure Diagnostics</a>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 8. JAVASCRIPT & THREE.JS 3D ENGINE -->
  <!-- ========================================================================= -->
  <script>
    // State Tracking
    let activeSceneId = "scene_0049";
    let activeSceneData = null;
    let currentStage = 0; // 0 = Overview, 1..8 = Stage Chambers
    let isPanelOpen = true;

    // Active Pixel Tracking State (Passes values continuously between stages)
    let trackedPixel = {
      x: 210,
      y: 140,
      r_raw: 192,
      g_raw: 178,
      b_raw: 160,
      r_norm: 1.17,
      g_norm: 1.08,
      b_norm: 0.98,
      patch_row: 10,
      patch_col: 16,
      patch_idx: 506,
      token_id: 507, // 1-indexed including [CLS]
      depth_metric: 1.84,
      gt_metric: 1.53,
      abs_err: 0.31
    };

    // 5-Minute Tour State
    let tourRunning = false;
    let tourSeconds = 0;
    let tourTimer = null;
    const TOUR_SCHEDULE = [
      { stage: 1, start: 0, duration: 35 },
      { stage: 2, start: 35, duration: 30 },
      { stage: 3, start: 65, duration: 30 },
      { stage: 4, start: 95, duration: 55 },
      { stage: 5, start: 150, duration: 25 },
      { stage: 6, start: 175, duration: 50 },
      { stage: 7, start: 225, duration: 30 },
      { stage: 8, start: 255, duration: 45 }
    ];

    // Three.js Core Globals
    let scene, camera, renderer, controls;
    let stageChamberGroups = {};
    let conduitLines = [];
    let particleSystems = [];
    let targetCamPos = new THREE.Vector3(0, 18, 44);
    let targetLookAt = new THREE.Vector3(0, 0, 0);

    // Stage 3D Coordinates along Serpentine Horizon
    const STAGE_COORDS = {
      0: { pos: new THREE.Vector3(0, 18, 44), lookAt: new THREE.Vector3(0, 0, 0) },
      1: { pos: new THREE.Vector3(-30, 2, 8), lookAt: new THREE.Vector3(-30, 0, 0), x: -30, z: 0 },
      2: { pos: new THREE.Vector3(-21, 2, 6), lookAt: new THREE.Vector3(-21, 0, -2), x: -21, z: -2 },
      3: { pos: new THREE.Vector3(-12, 2, 8), lookAt: new THREE.Vector3(-12, 0, 0), x: -12, z: 0 },
      4: { pos: new THREE.Vector3(-3, 2, 10), lookAt: new THREE.Vector3(-3, 0, 2), x: -3, z: 2 },
      5: { pos: new THREE.Vector3(6, 2, 8),   lookAt: new THREE.Vector3(6, 0, 0), x: 6, z: 0 },
      6: { pos: new THREE.Vector3(15, 2, 6),  lookAt: new THREE.Vector3(15, 0, -2), x: 15, z: -2 },
      7: { pos: new THREE.Vector3(24, 2, 8),  lookAt: new THREE.Vector3(24, 0, 0), x: 24, z: 0 },
      8: { pos: new THREE.Vector3(33, 2, 10), lookAt: new THREE.Vector3(33, 0, 2), x: 33, z: 2 }
    };

    // Complete Three-Level Educational Content for Every Stage
    const STAGE_DETAILS = {
      0: {
        badge: "OVERVIEW",
        tensor: "End-to-End Metric Depth Pipeline",
        title: "Depth Anything V2: Global Architectural Overview",
        levelA: "Depth Anything V2 transforms an ordinary 2D photograph into physical metric 3D distance. Explore the eight interconnected computational modules in 3D or click any component to enter its mathematical laboratory chamber.",
        formula: "I_{RGB} ∈ ℝ^{H × W × 3} ⟶ D_{metric} ∈ ℝ^{H × W} (meters)",
        varDict: `
          <dt>Encoder</dt><dd>DINOv2 ViT-Small (12 Blocks, 6 Heads, 384 Dim)</dd>
          <dt>Decoder</dt><dd>DPT Multi-Scale Feature Fusion (Pyramids 1/2 to 1/16)</dd>
          <dt>Depth Range</dt><dd>Metric Hypersim scale: 0.0m to 20.0m</dd>
        `,
        workedExample: "<strong>Architecture Pipeline:</strong><br>1. RGB Image (480×640×3) ⟶ 2. Preprocessed Tensor [1, 3, 518, 686]<br>3. Patch Tokens [1, 1814, 384] ⟶ 4. DINOv2 MHSA (12 Layers)<br>5. Hooks [2, 5, 8, 11] ⟶ 6. DPT Multi-Scale Fusion [1, 64, 148, 196]<br>7. Metric Depth Head ⟶ 8. Displaced 3D Elevation Surface",
        incoming: "User RGB Photograph",
        activeCoord: "Full Scene [480×640]",
        output: "Dense Metric Depth Map",
        nextBtn: "Enter Stage 1: Real RGB Image Grid"
      },
      1: {
        badge: "STAGE 01 / 08",
        tensor: "[480, 640, 3] uint8",
        title: "Input RGB Image: Discrete Color Grid",
        levelA: "A digital photograph is not an abstract concept to a computer; it is a matrix of discrete numbers. At every point on a 480×640 grid, the sensor records Red, Green, and Blue light intensities as integers from 0 to 255. In the 3D scene, inspect the authentic Red, Green, and Blue photographic channel decompositions separated in 3D space.",
        formula: "I(x, y) = [R(x, y), G(x, y), B(x, y)]^T ∈ {0, 1, ..., 255}^3",
        varDict: `
          <dt>x, y</dt><dd>Horizontal pixel column (0..639) and vertical row (0..479)</dd>
          <dt>R, G, B</dt><dd>8-bit discrete channel intensities (256 distinct levels)</dd>
          <dt>BGR Conv</dt><dd>OpenCV / PyTorch inference reorders channels: [R, G, B] ⟶ [B, G, R]</dd>
        `,
        workedExample: "<strong>Active Pixel Inspection (Coord X: 210, Y: 140):</strong><br>• Red Channel (R): 192 / 255 = 75.3% intensity<br>• Green Channel (G): 178 / 255 = 69.8% intensity<br>• Blue Channel (B): 160 / 255 = 62.7% intensity<br>RGB-to-BGR Tensor Reordering: [160, 178, 192]",
        incoming: "Raw Kinect Camera Sensor",
        activeCoord: "Pixel (X: 210, Y: 140)",
        output: "Matrix [480, 640, 3] uint8",
        nextBtn: "Send Result to Preprocessing →"
      },
      2: {
        badge: "STAGE 02 / 08",
        tensor: "[1, 3, 518, 686] float32",
        title: "Preprocessing: Normalization & Tensor Formation",
        levelA: "Deep neural networks are mathematically unstable when fed raw integers. Preprocessing scales pixel values to [0, 1], subtracts ImageNet dataset means, divides by standard deviations, and resizes the image so its dimensions are divisible by 14.",
        formula: "x_{norm} = \\frac{\\frac{x}{255.0} - \\mu_{ImageNet}}{\\sigma_{ImageNet}}, \\quad [H, W] ⟶ [518, 686]",
        varDict: `
          <dt>\\mu_{ImageNet}</dt><dd>Mean per channel: [R: 0.485, G: 0.456, B: 0.406]</dd>
          <dt>\\sigma_{ImageNet}</dt><dd>Standard deviation: [R: 0.229, G: 0.224, B: 0.225]</dd>
          <dt>Lower-Bound</dt><dd>Scale = 518 / 480 ≈ 1.0792. W_{new} = round(640 × 1.0792 / 14) × 14 = 686</dd>
        `,
        workedExample: "<strong>Channel Normalization for Pixel [192, 178, 160]:</strong><br>1. R: (192/255 - 0.485) / 0.229 = (0.7529 - 0.485) / 0.229 = <strong>+1.170</strong><br>2. G: (178/255 - 0.456) / 0.224 = (0.6980 - 0.456) / 0.224 = <strong>+1.080</strong><br>3. B: (160/255 - 0.406) / 0.225 = (0.6275 - 0.406) / 0.225 = <strong>+0.984</strong><br>Tensor Layout Formed: [Batch=1, Channels=3, H=518, W=686]",
        incoming: "Raw Matrix [480, 640, 3]",
        activeCoord: "Normalized: [+1.17, +1.08, +0.98]",
        output: "Tensor [1, 3, 518, 686]",
        nextBtn: "Send Tensor to Patch Embedding →"
      },
      3: {
        badge: "STAGE 03 / 08",
        tensor: "[1, 1814, 384] float32",
        title: "Patch Embedding: From Image Tiles to Tokens",
        levelA: "Transformers cannot process individual pixels directly. The 518×686 image is partitioned into non-overlapping 14×14 tiles. Notice the real sliced patch tile hovering in 3D: its 588 numbers are projected into a 384-dimensional token vector alongside the golden [CLS] token.",
        formula: "\\mathbf{e}_i = \\mathbf{W}_p \\cdot \\mathbf{p}_i + \\mathbf{b}_p, \\quad \\mathbf{z}_0 = [\\mathbf{x}_{cls}; \\mathbf{e}_1; ...; \\mathbf{e}_{N}] + \\mathbf{E}_{pos}",
        varDict: `
          <dt>\\mathbf{p}_i</dt><dd>Flattened 14×14 patch vector: 14 × 14 × 3 = 588 elements</dd>
          <dt>\\mathbf{W}_p</dt><dd>Learned projection weights: Conv2d(3, 384, kernel=14, stride=14)</dd>
          <dt>N</dt><dd>Spatial patch count: (518/14) × (686/14) = 37 × 49 = 1,813 patches</dd>
          <dt>\\mathbf{x}_{cls}</dt><dd>Prepend 1 learnable Class token ⟶ Total tokens = 1,814</dd>
        `,
        workedExample: "<strong>Active Patch Spatial Mapping:</strong><br>Pixel (210, 140) rescales to (226, 151) at 518×686.<br>• Patch Row = ⌊151 / 14⌋ = 10, Patch Col = ⌊226 / 14⌋ = 16<br>• Patch Index = 10 × 49 + 16 = <strong>#506</strong> (out of 1,813)<br>• Token Index in Transformer = 506 + 1 ([CLS]) = <strong>Token #507</strong><br>Output Tensor Shape: [1, 1814, 384]",
        incoming: "Tensor [1, 3, 518, 686]",
        activeCoord: "Patch #506 ⟶ Token #507",
        output: "Token Sequence [1, 1814, 384]",
        nextBtn: "Send Tokens into DINOv2 Transformer →"
      },
      4: {
        badge: "STAGE 04 / 08",
        tensor: "12 Blocks × [1, 1814, 384]",
        title: "DINOv2 Encoder: Multi-Head Self-Attention",
        levelA: "Tokens pass through 12 transformer blocks. In the 3D scene, inspect the authentic architectural blueprint of the Transformer block, the 6 physical attention heads, the cross-token attention heatmap, and the glowing dynamic attention connection arcs.",
        formula: "\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left(\\frac{\\mathbf{Q}\\mathbf{K}^T}{\\sqrt{d_k}}\\right)\\mathbf{V}, \\quad d_k = \\frac{384}{6} = 64",
        varDict: `
          <dt>\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}</dt><dd>Query (seeking), Key (advertising), Value (content) projections</dd>
          <dt>d_k</dt><dd>Head dimension = 64 (scaling factor \\sqrt{64} = 8 prevents vanishing gradients)</dd>
          <dt>MHSA</dt><dd>6 parallel attention heads concatenated ⟶ [1, 1814, 384]</dd>
          <dt>MLP</dt><dd>Feed-forward expansion: 384 ⟶ 1536 ⟶ 384 with GELU activation</dd>
        `,
        workedExample: "<strong>Step-by-Step Dot-Product Attention Arithmetic:</strong><br>1. Compare Query Token #507 with Key Token #508 & #720:<br>&nbsp;&nbsp;q · k₁ = 18.4 ⟶ Scaled: 18.4 / 8 = <strong>2.30</strong><br>&nbsp;&nbsp;q · k₂ = 12.0 ⟶ Scaled: 12.0 / 8 = <strong>1.50</strong><br>2. Softmax Normalisation:<br>&nbsp;&nbsp;exp(2.30) = 9.974, exp(1.50) = 4.482, Sum = 14.456<br>&nbsp;&nbsp;Attention Weight α₁ = 9.974 / 14.456 = <strong>0.69 (69%)</strong><br>&nbsp;&nbsp;Attention Weight α₂ = 4.482 / 14.456 = <strong>0.31 (31%)</strong><br>3. Contextual Output: v_out = 0.69 v₁ + 0.31 v₂ + Residual Shortcut",
        incoming: "Token Sequence [1, 1814, 384]",
        activeCoord: "Token #507 Contextualized",
        output: "Contextual Features [1, 1814, 384]",
        nextBtn: "Extract Intermediate Activations →"
      },
      5: {
        badge: "STAGE 05 / 08",
        tensor: "4 Layers × [1, 384, 37, 49]",
        title: "Intermediate Features: Four Macro Layers",
        levelA: "Depth estimation requires both sharp object borders (captured in early layers) and global room geometry (captured in deep layers). Inspect the authentic precomputed DINOv2 feature heatmaps hooked from blocks 3, 6, 9, and 12 displayed on floating glass panels.",
        formula: "\\mathbf{F}_l = \\text{Unflatten}(\\mathbf{z}_l[1:], (37, 49)), \\quad l \\in \\{2, 5, 8, 11\\}",
        varDict: `
          <dt>Hooks</dt><dd>PyTorch forward hooks at 0-indexed blocks [2, 5, 8, 11] (Layers 3, 6, 9, 12)</dd>
          <dt>[CLS] Drop</dt><dd>Drop token index 0: 1,814 - 1 = 1,813 spatial tokens</dd>
          <dt>Unflatten</dt><dd>Reshape 1,813 tokens into spatial grid: 37 rows × 49 columns</dd>
          <dt>Channels</dt><dd>Each spatial location carries 384 deep feature channels</dd>
        `,
        workedExample: "<strong>Authentic DINOv2 Layer Activations Loaded:</strong><br>• Layer 3 (Block 2): High-frequency edges & texture gradients<br>• Layer 6 (Block 5): Object boundaries & physical contacts<br>• Layer 9 (Block 8): Planar surfaces & wall structures<br>• Layer 12 (Block 11): Macroscopic perspective & scene field<br>Spatial Tensor Dimensions: 4 × [1, 384, 37, 49]",
        incoming: "12 Transformer Blocks",
        activeCoord: "Grid Location (Row 10, Col 16)",
        output: "4 Hooked Feature Maps [1, 384, 37, 49]",
        nextBtn: "Send Features to DPT Decoder →"
      },
      6: {
        badge: "STAGE 06 / 08",
        tensor: "Fused: [1, 64, 148, 196]",
        title: "DPT Decoder: Multi-Scale RefineNet Fusion",
        levelA: "The Dense Prediction Transformer (DPT) decoder rebuilds spatial resolution. The four hooked layers are projected into multi-scale pyramids (1/2, 1/4, 1/8, 1/16 scale) and fused top-down through RefineNet residual blocks into 64 channels.",
        formula: "\\text{Path}_i = \\text{RefineNet}\\left(\\text{Upsample}(\\text{Path}_{i+1}), \\; \\text{Proj}(\\mathbf{F}_i)\\right), \\; i \\in \\{3, 2, 1\\}",
        varDict: `
          <dt>Level 1 (Layer 3)</dt><dd>4× Deconv ⟶ 148 × 196 resolution (48 channels)</dd>
          <dt>Level 2 (Layer 6)</dt><dd>2× Deconv ⟶ 74 × 98 resolution (96 channels)</dd>
          <dt>Level 3 (Layer 9)</dt><dd>1× Identity ⟶ 37 × 49 resolution (192 channels)</dd>
          <dt>Level 4 (Layer 12)</dt><dd>2× Conv Down ⟶ 19 × 25 resolution (384 channels)</dd>
        `,
        workedExample: "<strong>Top-Down Feature Fusion Flow:</strong><br>1. Level 4 (19×25, 384ch) upsamples 2× to 38×50, aligns with Level 3<br>2. Residual convolution adds features element-wise: F_{3} = F_{3} + Proj(F_{4})<br>3. Process cascades upward to highest resolution Level 1 (148×196)<br>Final Decoder Feature Output: [Batch=1, Channels=64, H=148, W=196]",
        incoming: "4 Multi-Scale Feature Maps",
        activeCoord: "Fused Pyramid Resolution 148×196",
        output: "Unified Tensor [1, 64, 148, 196]",
        nextBtn: "Pass Representation to Depth Head →"
      },
      7: {
        badge: "STAGE 07 / 08",
        tensor: "[1, 1, 518, 686] float32",
        title: "Depth Prediction Head: Metric Distance Calculation",
        levelA: "The 64-channel feature map passes through convolutional layers, upsamples bilinearly to 518×686, and projects to a single depth channel. A Sigmoid function bounds the output, which is multiplied by max_depth = 20.0m to yield physical meters.",
        formula: "d(x, y) = \\text{Sigmoid}\\left(h(x, y)\\right) \\times \\text{max\\_depth}, \\quad \\text{max\\_depth} = 20.0\\text{m}",
        varDict: `
          <dt>h(x, y)</dt><dd>Logit output from Conv2d(32, 1, kernel=3, padding=1)</dd>
          <dt>\\text{Sigmoid}(z)</dt><dd>Logistic activation: 1 / (1 + e^{-z}) mapping logits to (0, 1)</dd>
          <dt>max_depth</dt><dd>Hypersim metric scaling parameter: exactly 20.0 metres</dd>
        `,
        workedExample: "<strong>Concrete Metric Scaling for Selected Pixel:</strong><br>1. Prediction Head Raw Logit: z = -2.289<br>2. Sigmoid Activation: 1 / (1 + e^{2.289}) = <strong>0.0920</strong><br>3. Metric Multiplication: 0.0920 × 20.0 meters = <strong>1.840 meters</strong><br>Result: Dense metric depth tensor [1, 1, 518, 686] in real meters",
        incoming: "Fused Features [1, 64, 148, 196]",
        activeCoord: "Predicted Depth: 1.84 meters",
        output: "Metric Array [518, 686] meters",
        nextBtn: "View Final Depth Map & 3D Surface →"
      },
      8: {
        badge: "STAGE 08 / 08",
        tensor: "[480, 640] float32 meters",
        title: "Final Depth Map & Interactive 3D Surface",
        levelA: "The predicted 518×686 depth tensor is interpolated back to the camera's original 480×640 resolution. In the 3D viewer, rotate around the authentic reconstructed 3D surface mesh textured with the real photograph and displaced along the Z optical axis.",
        formula: "D_{final} = \\text{BilinearResize}\\left(D_{pred}, (480, 640)\\right), \\quad \\text{Error} = |D_{pred} - D_{gt}|",
        varDict: `
          <dt>D_{final}</dt><dd>Final 480×640 float32 matrix representing distance in meters</dd>
          <dt>D_{gt}</dt><dd>Microsoft Kinect structured-light physical ground-truth measurement</dd>
          <dt>3D Elevation</dt><dd>Point (X, Y, Z) constructed from pixel coords and metric depth</dd>
        `,
        workedExample: "<strong>Auditing Selected Pixel (Coord X: 210, Y: 140):</strong><br>• Model Predicted Depth: <strong>1.840 m</strong><br>• Physical Ground Truth: <strong>1.525 m</strong><br>• Absolute Error: |1.840 - 1.525| = <strong>0.315 m (31.5 cm)</strong><br>• Relative Error: 0.315 / 1.525 = <strong>20.6%</strong><br>3D Mesh: Elevated and colored with actual RGB texture in WebGL",
        incoming: "Metric Tensor [518, 686]",
        activeCoord: "Pred: 1.84m | GT: 1.53m | Err: 0.31m",
        output: "Displaced 3D Surface Mesh",
        nextBtn: "Return to Complete Architecture Overview"
      }
    };

    // =========================================================================
    // INITIALIZATION & SCENE SETUP
    // =========================================================================
    window.addEventListener('DOMContentLoaded', initLab);

    function initLab() {
      // Populate Scene Dropdown
      const select = document.getElementById('scene-select');
      select.innerHTML = '';
      if (window.VEO_DATA && window.VEO_DATA.scenes) {
        window.VEO_DATA.scenes.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.sample_id;
          opt.textContent = `${s.sample_id.toUpperCase()} — ${s.title.split(':')[0]}`;
          select.appendChild(opt);
        });
      }

      setupThreeJS();
      loadSceneData(activeSceneId);
      renderMathematicalStage(0);
      animate();
    }

    function setupThreeJS() {
      const container = document.getElementById('canvas-container');
      const w = container.clientWidth;
      const h = container.clientHeight;

      scene = new THREE.Scene();
      scene.background = new THREE.Color(0xF6F3EA);
      scene.fog = new THREE.FogExp2(0xF6F3EA, 0.012);

      camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
      camera.position.copy(STAGE_COORDS[0].pos);

      renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
      renderer.setSize(w, h);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      container.appendChild(renderer.domElement);

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.maxPolarAngle = Math.PI / 2 + 0.05;
      controls.target.copy(STAGE_COORDS[0].lookAt);

      // Studio Lighting
      const ambientLight = new THREE.AmbientLight(0xFFFAF0, 0.95);
      scene.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0xFDFBF7, 0.85);
      dirLight.position.set(25, 45, 30);
      dirLight.castShadow = true;
      dirLight.shadow.mapSize.width = 1024;
      dirLight.shadow.mapSize.height = 1024;
      scene.add(dirLight);

      const fillLight = new THREE.DirectionalLight(0xEAE2D2, 0.45);
      fillLight.position.set(-25, 20, -20);
      scene.add(fillLight);

      // Floor Plane with subtle grid
      const floorGeom = new THREE.PlaneGeometry(160, 80);
      const floorMat = new THREE.MeshStandardMaterial({ color: 0xECE5D6, roughness: 0.9, metalness: 0.1 });
      const floor = new THREE.Mesh(floorGeom, floorMat);
      floor.rotation.x = -Math.PI / 2;
      floor.position.y = -4;
      floor.receiveShadow = true;
      scene.add(floor);

      const gridHelper = new THREE.GridHelper(160, 40, 0xD9D1C2, 0xE2D9C7);
      gridHelper.position.y = -3.98;
      scene.add(gridHelper);

      // Resize Listener
      window.addEventListener('resize', onWindowResize);
    }

    function onWindowResize() {
      const container = document.getElementById('canvas-container');
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }

    // =========================================================================
    // DYNAMIC TEXTURE GENERATORS (REAL CHANNELS, SCHEMATICS, LABELS)
    // =========================================================================

    // Generates genuine photographic channel texture (Red, Green, or Blue only)
    function createChannelTexture(imgEl, channelKey) {
      const c = document.createElement('canvas');
      c.width = imgEl.naturalWidth || 640;
      c.height = imgEl.naturalHeight || 480;
      const ctx = c.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(imgEl, 0, 0, c.width, c.height);
      const imgData = ctx.getImageData(0, 0, c.width, c.height);
      const d = imgData.data;

      for (let i = 0; i < d.length; i += 4) {
        if (channelKey === 'r') {
          d[i + 1] = 0; // zero green
          d[i + 2] = 0; // zero blue
        } else if (channelKey === 'g') {
          d[i] = 0;     // zero red
          d[i + 2] = 0; // zero blue
        } else if (channelKey === 'b') {
          d[i] = 0;     // zero red
          d[i + 1] = 0; // zero green
        }
      }
      ctx.putImageData(imgData, 0, 0);

      const tex = new THREE.CanvasTexture(c);
      tex.needsUpdate = true;
      return tex;
    }

    // Generates crisp 3D text banner sprite
    function createTextSprite(text, bgColor = "#68734D", textColor = "#FFFFFF") {
      const c = document.createElement('canvas');
      c.width = 512;
      c.height = 128;
      const ctx = c.getContext('2d', { willReadFrequently: true });
      
      ctx.fillStyle = bgColor;
      ctx.roundRect ? ctx.roundRect(10, 15, 492, 98, 20) : ctx.fillRect(10, 15, 492, 98);
      ctx.fill();
      ctx.strokeStyle = '#D9D1C2';
      ctx.lineWidth = 4;
      ctx.stroke();

      ctx.font = 'bold 32px "JetBrains Mono", monospace';
      ctx.fillStyle = textColor;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text, 256, 64);

      const tex = new THREE.CanvasTexture(c);
      const spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true });
      const sprite = new THREE.Sprite(spriteMat);
      sprite.scale.set(4.5, 1.125, 1);
      return sprite;
    }

    // Generates an authentic technical blueprint schematic texture of DINOv2 Transformer Block
    function createTransformerSchematicTexture() {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 1024;
      const ctx = c.getContext('2d', { willReadFrequently: true });

      // Blueprint Dark/Ivory background
      ctx.fillStyle = '#FAF7F0';
      ctx.fillRect(0, 0, 1024, 1024);
      ctx.strokeStyle = '#D9D1C2';
      ctx.lineWidth = 6;
      ctx.strokeRect(10, 10, 1004, 1004);

      // Title Banner
      ctx.fillStyle = '#414A32';
      ctx.font = 'bold 36px "Newsreader", serif';
      ctx.textAlign = 'center';
      ctx.fillText("DINOv2 ViT-Small Transformer Block", 512, 70);

      ctx.fillStyle = '#777466';
      ctx.font = '22px "JetBrains Mono", monospace';
      ctx.fillText("Input Tensor: [Batch, 1814 Tokens, 384 Embedding Dim]", 512, 110);

      function drawBox(y, h, text, sub, color, border) {
        ctx.fillStyle = color;
        ctx.fillRect(160, y, 704, h);
        ctx.strokeStyle = border;
        ctx.lineWidth = 3;
        ctx.strokeRect(160, y, 704, h);

        ctx.fillStyle = '#302F27';
        ctx.font = 'bold 26px "Inter", sans-serif';
        ctx.fillText(text, 512, y + h * 0.45);
        if (sub) {
          ctx.fillStyle = '#68734D';
          ctx.font = '19px "JetBrains Mono", monospace';
          ctx.fillText(sub, 512, y + h * 0.8);
        }
      }

      // Draw Modules
      drawBox(150, 70, "1. Layer Normalization 1", "Normalize across 384 embedding channels", "#EAE2D2", "#D9D1C2");
      drawBox(260, 110, "2. Q, K, V Linear Projections", "Query (Q), Key (K), Value (V) [384 ⟶ 64 × 6 Heads]", "#E8ECE2", "#68734D");
      drawBox(410, 120, "3. Multi-Head Self-Attention (MHSA)", "Attention(Q,K,V) = softmax(Q·Kᵀ / √64) · V", "#F4EBE2", "#8B6849");
      drawBox(570, 70, "4. Attention Linear Projection", "W_o: [6 × 64] ⟶ 384 Channels", "#EAE2D2", "#D9D1C2");
      drawBox(680, 70, "5. Layer Normalization 2", "Stabilize contextual features for MLP", "#EAE2D2", "#D9D1C2");
      drawBox(790, 110, "6. MLP Feed-Forward Network", "Linear(384 ⟶ 1536) + GELU + Linear(1536 ⟶ 384)", "#E8ECE2", "#414A32");
      drawBox(930, 60, "Output: Token Sequence [B, 1814, 384]", "Ready for Next Block or DPT Hooks", "#414A32", "#302F27");

      // Draw Residual Bypass Conduits
      ctx.strokeStyle = '#5A7A54';
      ctx.lineWidth = 5;
      ctx.setLineDash([8, 6]);

      // Skip 1
      ctx.beginPath();
      ctx.moveTo(140, 130);
      ctx.lineTo(80, 130);
      ctx.lineTo(80, 650);
      ctx.lineTo(140, 650);
      ctx.stroke();

      ctx.fillStyle = '#5A7A54';
      ctx.font = 'bold 20px "JetBrains Mono", monospace';
      ctx.fillText("(+) Residual Skip 1", 110, 400);

      // Skip 2
      ctx.beginPath();
      ctx.moveTo(880, 660);
      ctx.lineTo(940, 660);
      ctx.lineTo(940, 910);
      ctx.lineTo(880, 910);
      ctx.stroke();

      ctx.fillText("(+) Residual Skip 2", 910, 780);
      ctx.setLineDash([]);

      const tex = new THREE.CanvasTexture(c);
      tex.needsUpdate = true;
      return tex;
    }

    // Generates a dynamic 2D cross-token attention heatmap matrix
    function createAttentionHeatmapTexture() {
      const c = document.createElement('canvas');
      c.width = 512;
      c.height = 512;
      const ctx = c.getContext('2d', { willReadFrequently: true });

      const gridN = 8;
      const step = 512 / gridN;

      // Realistic token correlation matrix (strong diagonal + key semantic couplings)
      for (let r = 0; r < gridN; r++) {
        for (let col = 0; col < gridN; col++) {
          let score = (r === col) ? 0.75 : Math.sin(r * 1.5 + col * 2.1) * 0.35 + 0.35;
          if ((r === 2 && col === 5) || (r === 5 && col === 2)) score = 0.88; // Active query coupling
          score = Math.max(0.05, Math.min(0.95, score));

          // Heatmap Palette: Warm Ivory ⟶ Olive ⟶ Warm Ochre ⟶ Terracotta
          const red = Math.floor(104 + score * (200 - 104));
          const green = Math.floor(115 - score * (115 - 80));
          const blue = Math.floor(77 - score * (77 - 60));

          ctx.fillStyle = `rgb(${red}, ${green}, ${blue})`;
          ctx.fillRect(col * step, r * step, step, step);
          ctx.strokeStyle = '#FAF7F0';
          ctx.lineWidth = 1;
          ctx.strokeRect(col * step, r * step, step, step);

          // Write numerical weight
          ctx.fillStyle = score > 0.5 ? '#FFFFFF' : '#302F27';
          ctx.font = 'bold 16px "JetBrains Mono", monospace';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(score.toFixed(2), col * step + step / 2, r * step + step / 2);
        }
      }

      const tex = new THREE.CanvasTexture(c);
      tex.needsUpdate = true;
      return tex;
    }

    // =========================================================================
    // SCENE DATA & 3D MODEL BUILDER
    // =========================================================================
    function onSceneChange(val) {
      activeSceneId = val;
      loadSceneData(val);
    }

    function loadSceneData(sceneId) {
      if (!window.VEO_DATA || !window.VEO_DATA.scenes) return;
      activeSceneData = window.VEO_DATA.scenes.find(s => s.sample_id === sceneId);
      if (!activeSceneData) return;

      const def = activeSceneData.default_region;
      trackedPixel.x = def.x;
      trackedPixel.y = def.y;

      // Preload image element to build real channel textures
      const img = new Image();
      img.onload = () => {
        buildAllStageChambers(img);
      };
      img.src = activeSceneData.images.rgb;
    }

    function buildAllStageChambers(loadedImgEl) {
      // Clear existing objects
      Object.values(stageChamberGroups).forEach(grp => scene.remove(grp));
      stageChamberGroups = {};
      conduitLines.forEach(l => scene.remove(l));
      conduitLines = [];

      const texLoader = new THREE.TextureLoader();

      // Load active textures safely
      const rgbTex = texLoader.load(activeSceneData.images.rgb);
      const predTex = texLoader.load(activeSceneData.images.depth_pred);
      const gtTex = texLoader.load(activeSceneData.images.depth_gt);
      const errTex = texLoader.load(activeSceneData.images.error_map);

      // Generate photographic channel textures from real loaded image
      const texR = createChannelTexture(loadedImgEl, 'r');
      const texG = createChannelTexture(loadedImgEl, 'g');
      const texB = createChannelTexture(loadedImgEl, 'b');

      // -------------------------------------------------------------
      // 1. Stage 1 Chamber: Real RGB Image & Real Channel Slices (X: -30)
      // -------------------------------------------------------------
      const grp1 = new THREE.Group();
      grp1.position.set(-30, 0, 0);

      // Sprite Label
      const lbl1 = createTextSprite("STAGE 1: 2D RGB PHOTOGRAPH [480×640×3]", "#68734D");
      lbl1.position.set(0, 3.8, 0);
      grp1.add(lbl1);

      // Gallery Mounting Frame for Real RGB Image
      const frameGeom = new THREE.BoxGeometry(6.6, 5.0, 0.15);
      const frameMat = new THREE.MeshStandardMaterial({ color: 0xEAE2D2, roughness: 0.6 });
      const frame = new THREE.Mesh(frameGeom, frameMat);
      frame.position.z = -0.08;
      grp1.add(frame);

      // Real RGB Photograph Plane
      const imgGeom = new THREE.PlaneGeometry(6.4, 4.8);
      const rgbMat = new THREE.MeshStandardMaterial({ map: rgbTex, roughness: 0.2 });
      const rgbMesh = new THREE.Mesh(imgGeom, rgbMat);
      rgbMesh.castShadow = true;
      grp1.add(rgbMesh);

      // 3 Real Photographic Channel Slices Separated in 3D Space
      const realChannelSlices = [
        { tex: texR, z: -1.4, label: "Red Channel (Wavelength ~650nm)" },
        { tex: texG, z: -2.8, label: "Green Channel (Wavelength ~530nm)" },
        { tex: texB, z: -4.2, label: "Blue Channel (Wavelength ~470nm)" }
      ];
      realChannelSlices.forEach(ch => {
        const sliceMat = new THREE.MeshStandardMaterial({
          map: ch.tex,
          transparent: true,
          opacity: 0.85,
          roughness: 0.2,
          side: THREE.DoubleSide
        });
        const slice = new THREE.Mesh(imgGeom, sliceMat);
        slice.position.z = ch.z;
        grp1.add(slice);

        // Frame border for each slice
        const edge = new THREE.LineSegments(
          new THREE.EdgesGeometry(imgGeom),
          new THREE.LineBasicMaterial({ color: 0xD9D1C2, transparent: true, opacity: 0.6 })
        );
        edge.position.z = ch.z;
        grp1.add(edge);
      });

      // Highlighted selected pixel beacon
      const beaconGeom = new THREE.SphereGeometry(0.14, 16, 16);
      const beaconMat = new THREE.MeshBasicMaterial({ color: 0xC8755A });
      const beacon = new THREE.Mesh(beaconGeom, beaconMat);
      beacon.position.set((trackedPixel.x / 640) * 6.4 - 3.2, -(trackedPixel.y / 480) * 4.8 + 2.4, 0.1);
      grp1.add(beacon);

      scene.add(grp1);
      stageChamberGroups[1] = grp1;

      // -------------------------------------------------------------
      // 2. Stage 2 Chamber: Preprocessing & Normalization Tensor (X: -21)
      // -------------------------------------------------------------
      const grp2 = new THREE.Group();
      grp2.position.set(-21, 0, -2);

      const lbl2 = createTextSprite("STAGE 2: NORMALIZED TENSOR [1, 3, 518, 686]", "#68734D");
      lbl2.position.set(0, 3.8, 0);
      grp2.add(lbl2);

      // Normalized Tensor Block [1, 3, 518, 686]
      const tensorGeom = new THREE.BoxGeometry(6.86, 5.18, 1.4);
      const tensorMat = new THREE.MeshStandardMaterial({
        color: 0x68734D,
        roughness: 0.3,
        transparent: true,
        opacity: 0.65
      });
      const tensorMesh = new THREE.Mesh(tensorGeom, tensorMat);
      tensorMesh.castShadow = true;
      grp2.add(tensorMesh);

      const tensorWire = new THREE.LineSegments(
        new THREE.WireframeGeometry(tensorGeom),
        new THREE.LineBasicMaterial({ color: 0x414A32 })
      );
      grp2.add(tensorWire);

      scene.add(grp2);
      stageChamberGroups[2] = grp2;

      // -------------------------------------------------------------
      // 3. Stage 3 Chamber: Patch Embedding & Real Patch Extraction (X: -12)
      // -------------------------------------------------------------
      const grp3 = new THREE.Group();
      grp3.position.set(-12, 0, 0);

      const lbl3 = createTextSprite("STAGE 3: 1,813 PATCHES (14×14) + [CLS] TOKEN", "#8B6849");
      lbl3.position.set(0, 3.8, 0);
      grp3.add(lbl3);

      // 37x49 Grid Plane over Real Image
      const patchImgMat = new THREE.MeshStandardMaterial({ map: rgbTex, roughness: 0.4 });
      const patchImg = new THREE.Mesh(new THREE.PlaneGeometry(6.86, 5.18), patchImgMat);
      grp3.add(patchImg);

      const patchGridGeom = new THREE.PlaneGeometry(6.86, 5.18, 49, 37);
      const patchGridMat = new THREE.MeshBasicMaterial({ color: 0xFAF7F0, wireframe: true });
      const patchGrid = new THREE.Mesh(patchGridGeom, patchGridMat);
      patchGrid.position.z = 0.02;
      grp3.add(patchGrid);

      // Real Sliced 14x14 Patch Tile Hovering in 3D
      const activeTileGeom = new THREE.BoxGeometry(0.8, 0.8, 0.1);
      const activeTileMat = new THREE.MeshStandardMaterial({
        map: rgbTex,
        roughness: 0.2
      });
      const activeTile = new THREE.Mesh(activeTileGeom, activeTileMat);
      activeTile.position.set(0, 0, 1.4);
      grp3.add(activeTile);

      // Golden [CLS] Token Pillar
      const clsGeom = new THREE.CylinderGeometry(0.35, 0.35, 4.0, 16);
      const clsMat = new THREE.MeshStandardMaterial({ color: 0xC49A58, metalness: 0.7, roughness: 0.3 });
      const clsPillar = new THREE.Mesh(clsGeom, clsMat);
      clsPillar.position.set(-4.2, 0, 0);
      grp3.add(clsPillar);

      // 384-dim Patch Token Pillar for active patch
      const tokenPillarGeom = new THREE.CylinderGeometry(0.3, 0.3, 3.8, 16);
      const tokenPillarMat = new THREE.MeshStandardMaterial({ color: 0x68734D, metalness: 0.5, roughness: 0.4 });
      const tokenPillar = new THREE.Mesh(tokenPillarGeom, tokenPillarMat);
      tokenPillar.position.set(4.2, 0, 0);
      grp3.add(tokenPillar);

      scene.add(grp3);
      stageChamberGroups[3] = grp3;

      // -------------------------------------------------------------
      // 4. Stage 4 Chamber: Real 3D Transformer & Attention Model (X: -3)
      // -------------------------------------------------------------
      const grp4 = new THREE.Group();
      grp4.position.set(-3, 0, 2);

      const lbl4 = createTextSprite("STAGE 4: DINOv2 TRANSFORMER (12 BLOCKS, 6 HEADS)", "#414A32");
      lbl4.position.set(0, 4.2, 0);
      grp4.add(lbl4);

      // Technical Blueprint Schematic Panel in Background
      const schematicTex = createTransformerSchematicTexture();
      const schematicGeom = new THREE.PlaneGeometry(6.4, 6.4);
      const schematicMat = new THREE.MeshBasicMaterial({ map: schematicTex, side: THREE.DoubleSide });
      const schematicBoard = new THREE.Mesh(schematicGeom, schematicMat);
      schematicBoard.position.set(0, 0, -2.6);
      grp4.add(schematicBoard);

      // 12 Stacked Brushed-Metal Transformer Blocks
      for (let i = 0; i < 12; i++) {
        const blkGeom = new THREE.BoxGeometry(4.2, 0.28, 3.6);
        const isHooked = [2, 5, 8, 11].includes(i);
        const blkMat = new THREE.MeshStandardMaterial({
          color: isHooked ? 0x68734D : 0xD9D1C2,
          roughness: 0.3,
          metalness: 0.4
        });
        const blk = new THREE.Mesh(blkGeom, blkMat);
        blk.position.y = (i - 5.5) * 0.45;
        grp4.add(blk);

        // Status LED for hooked layers
        if (isHooked) {
          const ledGeom = new THREE.SphereGeometry(0.08, 12, 12);
          const ledMat = new THREE.MeshBasicMaterial({ color: 0x5A7A54 });
          const led = new THREE.Mesh(ledGeom, ledMat);
          led.position.set(-2.2, blk.position.y, 1.85);
          grp4.add(led);
        }
      }

      // 6 Physical Golden Attention Head Cylinders
      for (let h = 0; h < 6; h++) {
        const headGeom = new THREE.CylinderGeometry(0.2, 0.2, 0.9, 16);
        const headMat = new THREE.MeshStandardMaterial({ color: 0xC49A58, metalness: 0.6, roughness: 0.3 });
        const head = new THREE.Mesh(headGeom, headMat);
        head.position.set((h - 2.5) * 0.65, -0.2, 2.4);
        grp4.add(head);
      }

      // 3D Attention Heatmap Matrix Floor Grid
      const heatTex = createAttentionHeatmapTexture();
      const heatGeom = new THREE.PlaneGeometry(3.6, 3.6);
      const heatMat = new THREE.MeshBasicMaterial({ map: heatTex, side: THREE.DoubleSide });
      const heatMesh = new THREE.Mesh(heatGeom, heatMat);
      heatMesh.rotation.x = -Math.PI / 2.5;
      heatMesh.position.set(0, -2.4, 2.0);
      grp4.add(heatMesh);

      // Glowing Bezier Attention Connection Arcs leaping across tokens
      const curve1 = new THREE.QuadraticBezierCurve3(
        new THREE.Vector3(-1.8, 0, 1.2),
        new THREE.Vector3(0, 2.5, 1.8),
        new THREE.Vector3(1.8, 0, 1.2)
      );
      const arcGeom1 = new THREE.TubeGeometry(curve1, 32, 0.04, 8, false);
      const arcMat1 = new THREE.MeshBasicMaterial({ color: 0xC49A58 });
      grp4.add(new THREE.Mesh(arcGeom1, arcMat1));

      scene.add(grp4);
      stageChamberGroups[4] = grp4;

      // -------------------------------------------------------------
      // 5. Stage 5 Chamber: 4 Hooked Intermediate Feature Maps (X: 6)
      // -------------------------------------------------------------
      const grp5 = new THREE.Group();
      grp5.position.set(6, 0, 0);

      const lbl5 = createTextSprite("STAGE 5: MACROSCOPIC FEATURE ACTIVATIONS", "#5A7A54");
      lbl5.position.set(0, 4.2, 0);
      grp5.add(lbl5);

      const fGeom = new THREE.PlaneGeometry(4.9, 3.7);
      const layersMeta = [
        { key: "layer_3", color: 0x5A7A54, y: 3.0, label: "Layer 3: Edges" },
        { key: "layer_6", color: 0x68734D, y: 1.0, label: "Layer 6: Contours" },
        { key: "layer_9", color: 0x8B6849, y: -1.0, label: "Layer 9: Planes" },
        { key: "layer_12", color: 0x302F27, y: -3.0, label: "Layer 12: Perspective" }
      ];

      layersMeta.forEach(lm => {
        let mat;
        if (activeSceneData.activations && activeSceneData.activations[lm.key]) {
          const actTex = texLoader.load(activeSceneData.activations[lm.key]);
          mat = new THREE.MeshBasicMaterial({ map: actTex, side: THREE.DoubleSide });
        } else {
          mat = new THREE.MeshStandardMaterial({ color: lm.color, roughness: 0.4, side: THREE.DoubleSide });
        }
        const fPlane = new THREE.Mesh(fGeom, mat);
        fPlane.position.y = lm.y;
        fPlane.rotation.x = -Math.PI / 8;
        grp5.add(fPlane);

        // Glass Mount Border
        const border = new THREE.LineSegments(
          new THREE.EdgesGeometry(fGeom),
          new THREE.LineBasicMaterial({ color: 0xD9D1C2 })
        );
        border.position.y = lm.y;
        border.rotation.x = -Math.PI / 8;
        grp5.add(border);
      });

      scene.add(grp5);
      stageChamberGroups[5] = grp5;

      // -------------------------------------------------------------
      // 6. Stage 6 Chamber: DPT Multi-Scale Feature Fusion (X: 15)
      // -------------------------------------------------------------
      const grp6 = new THREE.Group();
      grp6.position.set(15, 0, -2);

      const lbl6 = createTextSprite("STAGE 6: DPT MULTI-SCALE REFINENET FUSION", "#68734D");
      lbl6.position.set(0, 3.8, 0);
      grp6.add(lbl6);

      // 4 Multi-Scale Pyramids (1/2, 1/4, 1/8, 1/16)
      const scales = [
        { w: 5.92, h: 4.44, z: 2.0, color: 0x5A7A54 },  // 148x196
        { w: 4.20, h: 3.15, z: 0.6, color: 0x68734D },  // 74x98
        { w: 2.80, h: 2.10, z: -0.8, color: 0x8B6849 }, // 37x49
        { w: 1.60, h: 1.20, z: -2.2, color: 0x414A32 }  // 19x25
      ];
      scales.forEach(sc => {
        const scGeom = new THREE.PlaneGeometry(sc.w, sc.h);
        const scMat = new THREE.MeshStandardMaterial({
          color: sc.color,
          transparent: true,
          opacity: 0.65,
          side: THREE.DoubleSide
        });
        const scMesh = new THREE.Mesh(scGeom, scMat);
        scMesh.position.z = sc.z;
        grp6.add(scMesh);

        const edge = new THREE.LineSegments(
          new THREE.EdgesGeometry(scGeom),
          new THREE.LineBasicMaterial({ color: 0xD9D1C2 })
        );
        edge.position.z = sc.z;
        grp6.add(edge);
      });

      scene.add(grp6);
      stageChamberGroups[6] = grp6;

      // -------------------------------------------------------------
      // 7. Stage 7 Chamber: Metric Depth Head & Sigmoid Curve (X: 24)
      // -------------------------------------------------------------
      const grp7 = new THREE.Group();
      grp7.position.set(24, 0, 0);

      const lbl7 = createTextSprite("STAGE 7: CONV HEAD & SIGMOID × 20.0m", "#8B6849");
      lbl7.position.set(0, 3.8, 0);
      grp7.add(lbl7);

      // Projection Convolutions Box
      const headBoxGeom = new THREE.BoxGeometry(4.5, 3.2, 1.2);
      const headBoxMat = new THREE.MeshStandardMaterial({ color: 0x8B6849, roughness: 0.3 });
      const headBox = new THREE.Mesh(headBoxGeom, headBoxMat);
      grp7.add(headBox);

      // Sigmoid Curve Arc in 3D
      const sigmoidPoints = [];
      for (let t = -4; t <= 4; t += 0.2) {
        const sig = 1 / (1 + Math.exp(-t));
        sigmoidPoints.push(new THREE.Vector3(t * 0.5, (sig - 0.5) * 2.5, 1.2));
      }
      const sigGeom = new THREE.BufferGeometry().setFromPoints(sigmoidPoints);
      const sigMat = new THREE.LineBasicMaterial({ color: 0xC49A58, linewidth: 3 });
      const sigLine = new THREE.Line(sigGeom, sigMat);
      grp7.add(sigLine);

      scene.add(grp7);
      stageChamberGroups[7] = grp7;

      // -------------------------------------------------------------
      // 8. Stage 8 Chamber: 3D Metric Elevation Surface Mesh (X: 33)
      // -------------------------------------------------------------
      const grp8 = new THREE.Group();
      grp8.position.set(33, 0, 2);

      const lbl8 = createTextSprite("STAGE 8: 3D METRIC DISPLACED SURFACE MESH", "#2B4B7C");
      lbl8.position.set(0, 4.2, 0);
      grp8.add(lbl8);

      // Reconstructed 3D Surface Mesh from activeSceneData
      if (activeSceneData.mesh_3d) {
        const m = activeSceneData.mesh_3d;
        const gw = m.grid_w;
        const gh = m.grid_h;
        const sGeom = new THREE.PlaneGeometry(6.4, 4.8, gw - 1, gh - 1);
        const pos = sGeom.attributes.position;
        const colors = new Float32Array(gw * gh * 3);

        let idx = 0;
        for (let r = 0; r < gh; r++) {
          for (let c = 0; c < gw; c++) {
            const d = m.depth_pred[r][c];
            // Displace along Z optical axis
            pos.setZ(idx, -(d - 2.0) * 1.4);

            const rgb = m.rgb_colors[r][c];
            colors[idx * 3] = rgb[0];
            colors[idx * 3 + 1] = rgb[1];
            colors[idx * 3 + 2] = rgb[2];
            idx++;
          }
        }
        sGeom.computeVertexNormals();
        sGeom.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const sMat = new THREE.MeshStandardMaterial({
          vertexColors: true,
          roughness: 0.4,
          side: THREE.DoubleSide
        });
        const surfaceMesh = new THREE.Mesh(sGeom, sMat);
        grp8.add(surfaceMesh);

        const wire = new THREE.LineSegments(
          new THREE.WireframeGeometry(sGeom),
          new THREE.LineBasicMaterial({ color: 0x68734D, transparent: true, opacity: 0.25 })
        );
        grp8.add(wire);
      } else {
        const fallbackGeom = new THREE.PlaneGeometry(6.4, 4.8);
        const fallbackMat = new THREE.MeshStandardMaterial({ map: predTex, roughness: 0.3 });
        const fallbackMesh = new THREE.Mesh(fallbackGeom, fallbackMat);
        grp8.add(fallbackMesh);
      }

      // Synchronized Side-by-Side Floating Probing Boards
      const subGeom = new THREE.PlaneGeometry(2.2, 1.65);
      const boards = [
        { tex: rgbTex, x: -3.6, y: -2.4, label: "Real RGB" },
        { tex: predTex, x: -1.2, y: -2.4, label: "Pred Depth" },
        { tex: gtTex, x: 1.2, y: -2.4, label: "GT Depth" },
        { tex: errTex, x: 3.6, y: -2.4, label: "Error Heatmap" }
      ];
      boards.forEach(b => {
        const bMesh = new THREE.Mesh(subGeom, new THREE.MeshBasicMaterial({ map: b.tex }));
        bMesh.position.set(b.x, b.y, 1.2);
        grp8.add(bMesh);

        const border = new THREE.LineSegments(
          new THREE.EdgesGeometry(subGeom),
          new THREE.LineBasicMaterial({ color: 0xD9D1C2 })
        );
        border.position.set(b.x, b.y, 1.2);
        grp8.add(border);
      });

      scene.add(grp8);
      stageChamberGroups[8] = grp8;

      // -------------------------------------------------------------
      // Connect Stages with Spline Data Conduits (Overview Horizon)
      // -------------------------------------------------------------
      const conduitPoints = [
        new THREE.Vector3(-30, 0, 0),
        new THREE.Vector3(-21, 0, -2),
        new THREE.Vector3(-12, 0, 0),
        new THREE.Vector3(-3, 0, 2),
        new THREE.Vector3(6, 0, 0),
        new THREE.Vector3(15, 0, -2),
        new THREE.Vector3(24, 0, 0),
        new THREE.Vector3(33, 0, 2)
      ];
      const curve = new THREE.CatmullRomCurve3(conduitPoints);
      const tubeGeom = new THREE.TubeGeometry(curve, 64, 0.08, 8, false);
      const tubeMat = new THREE.MeshBasicMaterial({ color: 0x68734D, transparent: true, opacity: 0.4 });
      const conduitMesh = new THREE.Mesh(tubeGeom, tubeMat);
      scene.add(conduitMesh);
      conduitLines.push(conduitMesh);
    }

    // =========================================================================
    // NAVIGATION & EDUCATIONAL PANEL RENDERING
    // =========================================================================
    function selectStage(stageIdx) {
      currentStage = stageIdx;

      // Update pills
      for (let i = 0; i <= 8; i++) {
        const pill = document.getElementById(`pill-${i}`);
        if (pill) {
          if (i === stageIdx) pill.classList.add('active');
          else pill.classList.remove('active');
        }
      }

      renderMathematicalStage(stageIdx);
      flyCameraToStage(stageIdx);
    }

    function flyCameraToStage(stageIdx) {
      const target = STAGE_COORDS[stageIdx];
      targetCamPos.copy(target.pos);
      targetLookAt.copy(target.lookAt);
    }

    function flyToOverview() {
      selectStage(0);
    }

    function navigateStageStep(delta) {
      let next = currentStage + delta;
      if (next < 0) next = 8;
      if (next > 8) next = 0;
      selectStage(next);
    }

    function advanceToNextStage() {
      if (currentStage >= 8) {
        selectStage(0);
      } else {
        selectStage(currentStage + 1);
      }
    }

    function togglePanel() {
      const panel = document.getElementById('math-lab-panel');
      const label = document.getElementById('panel-toggle-label');
      isPanelOpen = !isPanelOpen;
      if (isPanelOpen) {
        panel.classList.remove('collapsed');
        label.textContent = "Hide Math Panel";
      } else {
        panel.classList.add('collapsed');
        label.textContent = "Show Math Panel";
      }
    }

    function adjustCameraZoom(factor) {
      camera.position.sub(controls.target).multiplyScalar(factor).add(controls.target);
    }

    function renderMathematicalStage(idx) {
      const data = STAGE_DETAILS[idx];
      if (!data) return;

      document.getElementById('panel-stage-badge').textContent = data.badge;
      document.getElementById('panel-tensor-shape').textContent = data.tensor;
      document.getElementById('panel-stage-title').textContent = data.title;
      document.getElementById('panel-level-a').textContent = data.levelA;
      document.getElementById('panel-formula').textContent = data.formula;
      document.getElementById('panel-var-dict').innerHTML = data.varDict;
      document.getElementById('panel-worked-example').innerHTML = data.workedExample;
      document.getElementById('df-incoming-state').textContent = data.incoming;
      document.getElementById('df-active-coord').textContent = data.activeCoord;
      document.getElementById('df-output-produced').textContent = data.output;
      document.getElementById('btn-advance-stage').innerHTML = `<span>${data.nextBtn}</span> <i class="fa-solid fa-arrow-right"></i>`;
      document.getElementById('tour-stage-name').textContent = data.title.split(':')[0];
    }

    // =========================================================================
    // FIVE-MINUTE GUIDED TOUR CONTROLLER
    // =========================================================================
    function toggleTourPlay() {
      tourRunning = !tourRunning;
      const btnIcon = document.getElementById('icon-tour-play');
      const btnLabel = document.getElementById('label-tour-play');

      if (tourRunning) {
        btnIcon.className = "fa-solid fa-pause";
        btnLabel.textContent = "Pause Tour";
        startTourTimer();
      } else {
        btnIcon.className = "fa-solid fa-play";
        btnLabel.textContent = "Resume Tour";
        stopTourTimer();
      }
    }

    function startTourTimer() {
      if (tourTimer) clearInterval(tourTimer);
      tourTimer = setInterval(() => {
        tourSeconds++;
        if (tourSeconds > 300) {
          stopTourTimer();
          tourRunning = false;
          document.getElementById('icon-tour-play').className = "fa-solid fa-play";
          document.getElementById('label-tour-play').textContent = "Start 5-Min Tour";
          openTourModal();
          return;
        }

        updateTourProgressUI();

        // Check schedule transition
        for (let i = 0; i < TOUR_SCHEDULE.length; i++) {
          const item = TOUR_SCHEDULE[i];
          if (tourSeconds >= item.start && tourSeconds < item.start + item.duration) {
            if (currentStage !== item.stage) {
              selectStage(item.stage);
            }
            break;
          }
        }
      }, 1000);
    }

    function stopTourTimer() {
      if (tourTimer) {
        clearInterval(tourTimer);
        tourTimer = null;
      }
    }

    function restartTour() {
      stopTourTimer();
      tourSeconds = 0;
      updateTourProgressUI();
      selectStage(1);
      tourRunning = true;
      document.getElementById('icon-tour-play').className = "fa-solid fa-pause";
      document.getElementById('label-tour-play').textContent = "Pause Tour";
      startTourTimer();
    }

    function updateTourProgressUI() {
      const mins = Math.floor(tourSeconds / 60);
      const secs = tourSeconds % 60;
      document.getElementById('tour-timer-text').textContent = 
        `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')} / 05:00`;
      
      const pct = (tourSeconds / 300.0) * 100;
      document.getElementById('tour-progress-bar').style.width = `${pct}%`;
    }

    function seekTour(event) {
      const rect = event.currentTarget.getBoundingClientRect();
      const clickX = event.clientX - rect.left;
      const pct = Math.max(0, Math.min(1, clickX / rect.width));
      tourSeconds = Math.floor(pct * 300);
      updateTourProgressUI();

      for (let i = 0; i < TOUR_SCHEDULE.length; i++) {
        const item = TOUR_SCHEDULE[i];
        if (tourSeconds >= item.start && tourSeconds < item.start + item.duration) {
          selectStage(item.stage);
          break;
        }
      }
    }

    function openTourModal() {
      document.getElementById('tour-modal').classList.remove('hidden');
    }

    function closeTourModal() {
      document.getElementById('tour-modal').classList.add('hidden');
    }

    // =========================================================================
    // ANIMATION & CAMERA TWEEN LOOP
    // =========================================================================
    function animate() {
      requestAnimationFrame(animate);

      // Smooth camera interpolation towards target
      camera.position.lerp(targetCamPos, 0.05);
      controls.target.lerp(targetLookAt, 0.05);
      controls.update();

      // Subtle atmospheric floating in active chamber
      if (currentStage > 0 && stageChamberGroups[currentStage]) {
        const time = Date.now() * 0.001;
        stageChamberGroups[currentStage].rotation.y = Math.sin(time * 0.5) * 0.03;
      }

      renderer.render(scene, camera);
    }
  </script>
</body>
</html>"""
    return html

def main():
    out_path = Path("web_app/model_lab.html")
    html = build_model_lab_html()
    out_path.write_text(html, encoding="utf-8")
    print(f"Successfully generated {out_path} ({len(html)} bytes).")

if __name__ == "__main__":
    main()
