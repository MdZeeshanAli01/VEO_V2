from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def save_panel(rgb: np.ndarray, target: np.ndarray, prediction: np.ndarray, error_map: np.ndarray, output_path: Path, title: str) -> None:
    figure, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(rgb)
    axes[0].set_title("RGB")
    axes[1].imshow(prediction, cmap="magma")
    axes[1].set_title("Prediction")
    axes[2].imshow(target, cmap="magma")
    axes[2].set_title("NYU depth")
    axes[3].imshow(error_map, cmap="inferno")
    axes[3].set_title("Relative error")
    for axis in axes:
        axis.axis("off")
    figure.suptitle(title)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=120)
    plt.close(figure)