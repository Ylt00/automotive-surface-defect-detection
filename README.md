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
## Status

Dataset preparation is implemented and verified. Training, evaluation, visualization, and release stages will be added incrementally.
