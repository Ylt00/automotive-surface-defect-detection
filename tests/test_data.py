from pathlib import Path
import tempfile
import unittest

import cv2
import numpy as np

from defect_detection.data import prepare_neu_det
from defect_detection.dataset import validate_yolo_dataset


def _write_image(path: Path) -> None:
    image = np.full((200, 200, 3), 128, dtype=np.uint8)
    success, encoded = cv2.imencode(".jpg", image)
    if not success:
        raise RuntimeError("Could not encode test image")
    path.write_bytes(encoded.tobytes())


class DataPreparationTests(unittest.TestCase):
    def test_prepare_neu_det(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source" / "data" / "NEU-DET"
            for split, count in (("train", 3), ("test", 2)):
                images = source / split / "images"
                labels = source / split / "labels"
                images.mkdir(parents=True)
                labels.mkdir(parents=True)
                for index in range(count):
                    name = f"image_{index}"
                    _write_image(images / f"{name}.jpg")
                    (labels / f"{name}.txt").write_text(
                        f"{index % 6} 0.5 0.5 0.3 0.3\n",
                        encoding="utf-8",
                    )

            data_yaml, report_path, stats = prepare_neu_det(
                source_root=root / "source",
                output_root=root / "processed",
                report_path=root / "reports" / "stats.json",
                force=True,
            )
            report = validate_yolo_dataset(data_yaml)
            self.assertTrue(report.is_valid, report.errors)
            self.assertEqual(report.images, 5)
            self.assertEqual(stats["train_images"], 3)
            self.assertEqual(stats["val_images"], 2)
            self.assertTrue(report_path.exists())


if __name__ == "__main__":
    unittest.main()