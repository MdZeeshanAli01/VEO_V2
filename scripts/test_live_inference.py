import sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path("src").resolve()))
from veo_nyu.inference import OfficialMetricDepthPredictor

checkpoint = Path("checkpoints/depth_anything_v2_metric_hypersim_vits.pth")
repo = Path("official/Depth-Anything-V2")

print("Initializing Depth Anything V2 ViT-Small...")
predictor = OfficialMetricDepthPredictor(official_repo=repo, checkpoint=checkpoint, encoder="vits", device="cpu")

rgb = np.array(Image.open("data/nyu/splits/test/rgb/scene_0049.png"))
print("Running prediction on scene_0049 (480x640)...")
pred = predictor.predict(rgb)
print("Output prediction shape:", pred.shape, "range:", f"[{pred.min():.3f}, {pred.max():.3f}]")

