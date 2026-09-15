from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class DatasetConfig:
    name: str = "hypersim"
    rgb_dir: Path = Path("data/hypersim/rgb")
    depth_dir: Path = Path("data/hypersim/depth")
    manifest: Path | None = Path("data/hypersim/manifest.txt")
    depth_scale: float = 1000.0
    max_depth_m: float = 10.0
    split: str = "official_test"


@dataclass(frozen=True)
class ExperimentConfig:
    model_name: str = "precomputed"
    align_scale_shift: bool = False
    error_percentile: float = 85.0
    min_region_area: int = 25
    include_reflection: bool = True
    random_seed: int = 42


@dataclass(frozen=True)
class OutputConfig:
    directory: Path = Path("outputs")


@dataclass(frozen=True)
class Config:
    dataset: DatasetConfig = DatasetConfig()
    experiment: ExperimentConfig = ExperimentConfig()
    outputs: OutputConfig = OutputConfig()


def load_config(path: Path) -> Config:
    values = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    dataset_values = values.get("dataset", {})
    experiment_values = values.get("experiment", {})
    output_values = values.get("outputs", {})
    return Config(
        dataset=DatasetConfig(
            name=dataset_values.get("name", DatasetConfig.name),
            rgb_dir=Path(dataset_values.get("rgb_dir", DatasetConfig.rgb_dir)),
            depth_dir=Path(dataset_values.get("depth_dir", DatasetConfig.depth_dir)),
            manifest=Path(dataset_values["manifest"]) if dataset_values.get("manifest") else None,
            depth_scale=float(dataset_values.get("depth_scale", DatasetConfig.depth_scale)),
            max_depth_m=float(dataset_values.get("max_depth_m", DatasetConfig.max_depth_m)),
            split=dataset_values.get("split", DatasetConfig.split),
        ),
        experiment=ExperimentConfig(
            model_name=experiment_values.get("model_name", ExperimentConfig.model_name),
            align_scale_shift=bool(experiment_values.get("align_scale_shift", ExperimentConfig.align_scale_shift)),
            error_percentile=float(experiment_values.get("error_percentile", ExperimentConfig.error_percentile)),
            min_region_area=int(experiment_values.get("min_region_area", ExperimentConfig.min_region_area)),
            include_reflection=bool(experiment_values.get("include_reflection", ExperimentConfig.include_reflection)),
            random_seed=int(experiment_values.get("random_seed", ExperimentConfig.random_seed)),
        ),
        outputs=OutputConfig(directory=Path(output_values.get("directory", OutputConfig.directory))),
    )
