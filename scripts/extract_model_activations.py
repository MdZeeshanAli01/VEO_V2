import sys
from pathlib import Path
import numpy as np
import torch
import cv2
from PIL import Image

sys.path.insert(0, str(Path("src").resolve()))
sys.path.insert(0, str(Path("official/Depth-Anything-V2").resolve()))
sys.path.insert(0, str(Path("official/Depth-Anything-V2/metric_depth").resolve()))

from depth_anything_v2.dpt import DepthAnythingV2

checkpoint = Path("checkpoints/depth_anything_v2_metric_hypersim_vits.pth")
configs = {"encoder": "vits", "features": 64, "out_channels": [48, 96, 192, 384], "max_depth": 20.0}

print("Loading model...")
model = DepthAnythingV2(**configs)
model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
model.eval()

rgb = np.array(Image.open("data/nyu/splits/test/rgb/scene_0049.png"))
bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

# Hook into DINOv2 layers
activations = {}
def get_hook(name):
    def hook(m, inp, out):
        activations[name] = out
    return hook

# In DINOv2, blocks are model.pretrained.blocks[0..11]
# We want intermediate layers 2, 5, 8, 11 (which correspond to 3, 6, 9, 12)
target_blocks = [2, 5, 8, 11]
for idx in target_blocks:
    model.pretrained.blocks[idx].register_forward_hook(get_hook(f"block_{idx+1}"))

print("Running forward pass...")
with torch.no_grad():
    image, (h, w) = model.image2tensor(bgr, input_size=518)
    patch_h, patch_w = image.shape[-2] // 14, image.shape[-1] // 14
    depth = model.forward(image)

print(f"Captured {len(activations)} intermediate activations:")
for k, v in activations.items():
    print(f"  {k}: shape={v.shape}")
    # v is [B, N+1, D] where B=1, N=patch_h*patch_w=37*37=1369, D=384
    # Tokens without CLS: [B, N, D]
    tokens = v[:, 1:, :] # shape [1, 1369, 384]
    # Compute mean activation magnitude across feature channels
    feat_map = tokens[0].mean(dim=-1).reshape(patch_h, patch_w).numpy()
    print(f"  {k} spatial map shape: {feat_map.shape}, min={feat_map.min():.3f}, max={feat_map.max():.3f}")

print("Successfully extracted authentic model activations!")

