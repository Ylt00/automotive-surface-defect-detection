# YOLOv8n and P2 Defect Model Comparison

Date: 2026-09-18

## Objective

Compare YOLOv8n and YOLOv8n-P2 under an identical low-cost CPU protocol.

## Controlled Setup

- Training images: 1620
- Validation images: 180
- Image size: 128
- Batch size: 32
- Epochs: 3
- Device: CPU
- Seed: 42

The P2 model initializes compatible weights from the YOLOv8n checkpoint. The extra P2 layers start from random initialization.

## Results

| Model | Precision | Recall | mAP50 | mAP50-95 | Params | GFLOPs |
|---|---:|---:|---:|---:|---:|---:|
| YOLOv8n 128px | 0.344 | 0.487 | 0.387 | 0.172 | 3,006,818 | 8.1 |
| YOLOv8n-P2 128px | 0.628 | 0.312 | 0.284 | 0.102 | 2,921,832 | 12.2 |

## Result

P2 does not improve mAP under this low-cost CPU protocol. mAP50 decreases by 0.103 and mAP50-95 decreases by 0.070, while GFLOPs increase from 8.1 to 12.2.

## Interpretation

P2 increases the number of high-resolution prediction layers and improves precision, but recall drops substantially. The extra layers have only three epochs to adapt, and 128-pixel input reduces the information available to small defect regions. The full 224-pixel YOLOv8n baseline remains the strongest model in this project.

A fair future P2 evaluation should use GPU training, longer schedules, multiple seeds, and a compatible pretrained P2 checkpoint if available.