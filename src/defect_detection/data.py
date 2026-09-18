"""Prepare the NEU-DET dataset as a clean local YOLO dataset."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import yaml

from .classes import DEFECT_CLASS_NAMES
from .dataset import validate_yolo_dataset


NEU_DET_SOURCE_REPO = "Marfbin/NEU-DET-with-yolov8"
NEU_DET_SOURCE_SSH = "ssh://git@ssh.github.com:443/Marfbin/NEU-DET-with-yolov8.git"


def clone_neu_det_source(destination: str | Path) -> Path:
    """Clone only the NEU-DET data directory from the public source repository."""

    target = Path(destination).expanduser().resolve()
    if target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "git",
            "-c",
            "core.sshCommand=C:/Windows/System32/OpenSSH/ssh.exe",
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            NEU_DET_SOURCE_SSH,
            str(target),
        ],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(target), "sparse-checkout", "set", "data/NEU-DET"],
        check=True,
    )
    return target


def _find_neu_det_root(source_root: Path) -> Path:
    for candidate in (source_root / "data" / "NEU-DET", source_root / "NEU-DET", source_root):
        if (candidate / "train" / "images").is_dir() and (candidate / "test" / "images").is_dir():
            return candidate
    raise FileNotFoundError(f"Could not find NEU-DET train/test directories under {source_root}")


def _copy_split(source_root: Path, output_root: Path, source_split: str, target_split: str) -> int:
    images_dir = source_root / source_split / "images"
    labels_dir = source_root / source_split / "labels"
    target_images = output_root / "images" / target_split
    target_labels = output_root / "labels" / target_split
    target_images.mkdir(parents=True, exist_ok=True)
    target_labels.mkdir(parents=True, exist_ok=True)

    images = sorted(path for path in images_dir.iterdir() if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"})
    for image_path in images:
        label_path = labels_dir / image_path.with_suffix(".txt").name
        if not label_path.exists():
            raise FileNotFoundError(f"Missing label for {image_path}: {label_path}")
        shutil.copyfile(image_path, target_images / image_path.name)
        shutil.copyfile(label_path, target_labels / label_path.name)
    return len(images)


def prepare_neu_det(
    source_root: str | Path,
    output_root: str | Path,
    report_path: str | Path | None = None,
    force: bool = False,
) -> tuple[Path, Path, dict[str, object]]:
    """Copy NEU-DET into train/val YOLO structure and generate data.yaml."""

    source = _find_neu_det_root(Path(source_root).expanduser().resolve())
    output = Path(output_root).expanduser().resolve()
    if force and output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    train_count = _copy_split(source, output, "train", "train")
    val_count = _copy_split(source, output, "test", "val")

    data = {
        "path": output.as_posix(),
        "train": "images/train",
        "val": "images/val",
        "names": {index: name for index, name in enumerate(DEFECT_CLASS_NAMES)},
    }
    data_yaml = output / "data.yaml"
    data_yaml.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    validation = validate_yolo_dataset(data_yaml)
    stats: dict[str, object] = {
        "source_repository": NEU_DET_SOURCE_REPO,
        "source_root": source.name,
        "train_images": train_count,
        "val_images": val_count,
        "classes": list(DEFECT_CLASS_NAMES),
        "objects": validation.objects,
        "class_objects": validation.class_objects,
        "size_distribution": validation.size_distribution,
        "errors": validation.errors,
        "warnings": validation.warnings,
    }
    report = Path(report_path).expanduser().resolve() if report_path else output.parent / "neu-det-stats.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    return data_yaml, report, stats