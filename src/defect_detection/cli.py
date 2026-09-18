"""Command-line interface for the automotive defect detection project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .data import clone_neu_det_source, prepare_neu_det
from .dataset import validate_yolo_dataset


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="auto-defect", description="Automotive surface defect detection tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print the package version")

    clone_parser = subparsers.add_parser("clone-data", help="Clone the public NEU-DET data source")
    clone_parser.add_argument("--destination", default="data/raw/neu-det-source")

    prepare_parser = subparsers.add_parser("prepare-data", help="Prepare NEU-DET train/val data")
    prepare_parser.add_argument("--source", default="data/raw/neu-det-source")
    prepare_parser.add_argument("--output", default="data/processed/neu-det")
    prepare_parser.add_argument("--report", default="reports/neu-det-stats.json")
    prepare_parser.add_argument("--force", action="store_true")

    validate_parser = subparsers.add_parser("validate", help="Validate a YOLO dataset")
    validate_parser.add_argument("--data", required=True)

    train_parser = subparsers.add_parser("train", help="Train a YOLO model")
    train_parser.add_argument("--config", default="configs/neu-det-cpu.yaml")
    train_parser.add_argument("--model")
    train_parser.add_argument("--epochs", type=int)
    train_parser.add_argument("--imgsz", type=int)
    train_parser.add_argument("--device")
    train_parser.add_argument("--name")

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate YOLO weights")
    evaluate_parser.add_argument("--weights", required=True)
    evaluate_parser.add_argument("--data", required=True)
    evaluate_parser.add_argument("--imgsz", type=int, default=320)
    evaluate_parser.add_argument("--device", default="cpu")
    evaluate_parser.add_argument("--project", default="runs/val")
    evaluate_parser.add_argument("--name", default="neu-det-yolov8n")

    predict_parser = subparsers.add_parser("predict", help="Run YOLO inference")
    predict_parser.add_argument("--weights", required=True)
    predict_parser.add_argument("--source", required=True)
    predict_parser.add_argument("--imgsz", type=int, default=320)
    predict_parser.add_argument("--device", default="cpu")
    predict_parser.add_argument("--project", default="runs/predict")
    predict_parser.add_argument("--name", default="neu-det-yolov8n")
    predict_parser.add_argument("--conf", type=float, default=0.25)

    report_parser = subparsers.add_parser("report", help="Generate visual report assets")
    report_parser.add_argument("--images", required=True)
    report_parser.add_argument("--labels", required=True)
    report_parser.add_argument("--predictions", required=True)
    report_parser.add_argument("--metrics", required=True)
    report_parser.add_argument("--results", required=True)
    report_parser.add_argument("--plots", required=True)
    report_parser.add_argument("--assets", default="docs/assets")
    report_parser.add_argument("--analysis", default="docs/analysis")
    report_parser.add_argument("--limit", type=int, default=9)

    compare_parser = subparsers.add_parser("compare", help="Compare two evaluation metric files")
    compare_parser.add_argument("--reference-name", default="YOLOv8n baseline")
    compare_parser.add_argument("--reference-metrics", required=True)
    compare_parser.add_argument("--candidate-name", default="YOLOv8n-P2")
    compare_parser.add_argument("--candidate-metrics", required=True)
    compare_parser.add_argument("--output-json", default="reports/model-comparison.json")
    compare_parser.add_argument("--output-png", default="docs/analysis/model-comparison.png")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0

    if args.command == "clone-data":
        source = clone_neu_det_source(args.destination)
        print(f"Cloned NEU-DET source to: {source}")
        return 0

    if args.command == "prepare-data":
        data_yaml, report, stats = prepare_neu_det(
            source_root=args.source,
            output_root=args.output,
            report_path=args.report,
            force=args.force,
        )
        print(f"Prepared dataset: {data_yaml}")
        print(f"Report: {report}")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return 0

    if args.command == "validate":
        report = validate_yolo_dataset(args.data)
        print(json.dumps(report.as_dict(), indent=2, ensure_ascii=False))
        return 0 if report.is_valid else 1

    if args.command == "train":
        from .train import train_model

        train_model(
            args.config,
            overrides={
                "model": args.model,
                "epochs": args.epochs,
                "imgsz": args.imgsz,
                "device": args.device,
                "name": args.name,
            },
        )
        return 0

    if args.command == "evaluate":
        from .train import evaluate_model

        _, metrics_path = evaluate_model(
            weights=args.weights,
            data=args.data,
            imgsz=args.imgsz,
            device=args.device,
            project=args.project,
            name=args.name,
        )
        print(f"Metrics saved to: {metrics_path}")
        return 0

    if args.command == "predict":
        from .train import predict_model

        predict_model(
            weights=args.weights,
            source=args.source,
            imgsz=args.imgsz,
            device=args.device,
            project=args.project,
            name=args.name,
            conf=args.conf,
        )
        return 0

    if args.command == "report":
        from .visualize import build_visual_report

        report = build_visual_report(
            images_dir=args.images,
            labels_dir=args.labels,
            predictions_dir=args.predictions,
            metrics_path=args.metrics,
            results_csv=args.results,
            plots_dir=args.plots,
            assets_dir=args.assets,
            analysis_dir=args.analysis,
            limit=args.limit,
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    if args.command == "compare":
        from .compare import compare_models

        comparison = compare_models(
            reference_name=args.reference_name,
            reference_metrics=args.reference_metrics,
            candidate_name=args.candidate_name,
            candidate_metrics=args.candidate_metrics,
            output_json=args.output_json,
            output_png=args.output_png,
        )
        print(json.dumps(comparison, indent=2, ensure_ascii=False))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())