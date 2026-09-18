# Automotive Surface Defect Detection

YOLOv8-based surface defect detection for automotive and industrial quality inspection.

## Project Goals

- Prepare the public NEU-DET six-class defect dataset
- Validate images, labels, class IDs, and bounding boxes
- Train a YOLOv8n baseline
- Generate defect detection result images
- Generate per-class metrics and error cases
- Test a P2 high-resolution detection head for small defects
- Use unit tests and GitHub Actions
- Publish reproducible results and a GitHub Release

## Defect Classes

| ID | Class |
|---:|---|
| 0 | crazing |
| 1 | inclusion |
| 2 | patches |
| 3 | pitted_surface |
| 4 | rolled-in_scale |
| 5 | scratches |

## Planned Pipeline

- Dataset download and verification
- YOLO-format dataset validation
- YOLOv8n baseline training and evaluation
- Prediction-grid and defect-size analysis
- Confusion matrix and PR curves
- YOLOv8n-P2 comparison
- Documentation and release

## Dataset Notice

NEU-DET is a public research dataset. Raw images, labels, and converted datasets are not committed to this repository. The download script will preserve the original source and attribution. Dataset terms remain separate from the repository's MIT license.

## Prepared Dataset

| Item | Value |
|---|---:|
| Source | NEU-DET |
| Train images | 1620 |
| Validation images | 180 |
| Total images | 1800 |
| Retained objects | 4189 |
| Small objects | 447 |
| Medium objects | 2774 |
| Large objects | 968 |
| Validation errors | 0 |
## YOLOv8n Baseline

| Metric | Value |
|---|---:|
| Precision | 0.668 |
| Recall | 0.655 |
| mAP50 | 0.708 |
| mAP50-95 | 0.361 |

Training details are recorded in `docs/experiments/neu-det-yolov8n.md`.
## Detection Results

![Ground truth defects](docs/assets/ground-truth-grid.jpg)

![YOLOv8n predictions](docs/assets/prediction-grid.jpg)

![Small defect examples](docs/assets/small-object-grid.jpg)

## Evaluation Analysis

![Overall metrics](docs/analysis/overall-metrics.png)

![Training curves](docs/analysis/training-curves.png)

![Confusion matrix](docs/analysis/confusion-matrix.png)

![Precision recall curve](docs/analysis/precision-recall-curve.png)

![Defect size distribution](docs/analysis/defect-size-distribution.png)
## Status

The YOLOv8n baseline and visual report are complete. P2 comparison and release stages will be added later.
