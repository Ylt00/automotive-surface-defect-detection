# NEU-DET Dataset Preparation

## Source

The project uses the public NEU-DET surface defect dataset through the public repository `Marfbin/NEU-DET-with-yolov8`. The dataset source is kept separate from this repository and is not redistributed.

Source repository: https://github.com/Marfbin/NEU-DET-with-yolov8

## Classes

| ID | Class |
|---:|---|
| 0 | crazing |
| 1 | inclusion |
| 2 | patches |
| 3 | pitted_surface |
| 4 | rolled-in_scale |
| 5 | scratches |

## Prepared Split

| Split | Images |
|---|---:|
| Train | 1620 |
| Validation | 180 |
| Total | 1800 |

The source labels are already in normalized YOLO format. The preparation step validates them, copies the train/test split into a clean local train/val structure, and generates a local `data.yaml`.

## Commands

```powershell
python -m defect_detection.cli clone-data --destination data/raw/neu-det-source
python -m defect_detection.cli prepare-data --source data/raw/neu-det-source --output data/processed/neu-det --report reports/neu-det-stats.json --force
python -m defect_detection.cli validate --data data/processed/neu-det/data.yaml
```

## Licensing Note

The source repository is licensed separately. The original data source and attribution must be preserved. Raw images, labels, and processed datasets are excluded from this repository.