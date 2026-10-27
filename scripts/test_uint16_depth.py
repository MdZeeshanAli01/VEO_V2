import numpy as np
import base64

# Test with real GT depth from scene_0049
gt = np.load("data/nyu/splits/test/depth/scene_0049.npy") # shape (480, 640), float32 in meters

# Quantize to millimeters (uint16)
gt_mm = np.clip(np.round(gt * 1000.0), 0, 65535).astype(np.uint16)

# Encode to base64
b64 = base64.b64encode(gt_mm.tobytes()).decode("ascii")
print(f"Base64 string length: {len(b64):,} chars ({len(b64)/1024:.1f} KB)")

# Decode
raw_bytes = base64.b64decode(b64)
decoded_mm = np.frombuffer(raw_bytes, dtype=np.uint16).reshape(480, 640)
recovered = decoded_mm.astype(np.float32) / 1000.0

max_err_mm = np.max(np.abs(recovered - gt)) * 1000.0
print(f"Max reconstruction error: {max_err_mm:.4f} mm (less than half a millimeter!)")
print(f"Sample at (240, 320): Original={gt[240, 320]:.4f}m, Recovered={recovered[240, 320]:.4f}m")

