from pathlib import Path
from typing import Protocol

import numpy as np


class DepthPredictor(Protocol):
    def predict(self, rgb: np.ndarray) -> np.ndarray:
        """Return a depth array with the same height and width as the RGB image."""


class PrecomputedPredictor:
    def __init__(self, prediction_dir: Path):
        self.prediction_dir = prediction_dir

    def predict_for_sample(self, sample_id: str, expected_shape: tuple[int, int]) -> np.ndarray:
        path = self.prediction_dir / f"{sample_id}.npy"
        if not path.exists():
            raise FileNotFoundError(f"Missing prediction for {sample_id}: {path}")
        prediction = np.asarray(np.load(path), dtype=np.float32)
        if prediction.shape != expected_shape:
            raise ValueError(f"Prediction {path} has shape {prediction.shape}; expected {expected_shape}")
        return prediction


class TransformersDepthPredictor:
    def __init__(self, model_id: str, device: str = "auto"):
        try:
            import torch
            from transformers import pipeline
        except ImportError as exc:
            raise ImportError("Install the model extra with: pip install -e '.[model]'") from exc
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        pipeline_device = 0 if device == "cuda" else -1
        self._pipe = pipeline("depth-estimation", model=model_id, device=pipeline_device)

    def predict(self, rgb: np.ndarray) -> np.ndarray:
        from PIL import Image

        result = self._pipe(Image.fromarray(rgb))
        prediction = result["predicted_depth"].squeeze().detach().cpu().numpy().astype(np.float32)
        if prediction.shape != rgb.shape[:2]:
            import cv2

            prediction = cv2.resize(prediction, (rgb.shape[1], rgb.shape[0]))
        return prediction