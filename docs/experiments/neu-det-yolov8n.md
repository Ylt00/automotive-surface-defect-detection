# YOLOv8n NEU-DET Baseline

Date: 2026-09-18

## Objective

Establish a YOLOv8n baseline for six-class NEU-DET surface defect detection.

## Dataset

- Training images: 1620
- Validation images: 180
- Objects: 4189
- Classes: crazing, inclusion, patches, pitted_surface, rolled-in_scale, scratches

## Training

- Model: YOLOv8n pretrained
- Image size: 224
- Batch size: 32
- Epochs: 10
- Device: CPU
- Seed: 42

## Overall Metrics

| Metric | Value |
|---|---:|
| Precision | 0.668 |
| Recall | 0.655 |
| mAP50 | 0.708 |
| mAP50-95 | 0.361 |

## Per-Class Metrics

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| crazing | 0.844 | 0.137 | 0.376 | 0.144 |
| inclusion | 0.590 | 0.888 | 0.850 | 0.468 |
| patches | 0.771 | 0.939 | 0.946 | 0.573 |
| pitted_surface | 0.801 | 0.674 | 0.770 | 0.401 |
| rolled-in_scale | 0.496 | 0.464 | 0.496 | 0.196 |
| scratches | 0.507 | 0.828 | 0.807 | 0.386 |

## Interpretation

Crazing has low recall despite high precision, suggesting many subtle crack regions are missed. Rolled-in scale is also difficult. Patches and inclusion achieve the strongest mAP50 results.

## Outputs

- `runs/train/neu-det-yolov8n/weights/best.pt`
- `runs/train/neu-det-yolov8n/results.csv`
- `runs/val/neu-det-yolov8n/metrics.json`
- `runs/predict/neu-det-yolov8n/`