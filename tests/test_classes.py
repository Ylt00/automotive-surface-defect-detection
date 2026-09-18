import unittest

from defect_detection.classes import DEFECT_CLASS_NAMES


class DefectClassTests(unittest.TestCase):
    def test_expected_classes(self) -> None:
        self.assertEqual(
            DEFECT_CLASS_NAMES,
            ("crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"),
        )


if __name__ == "__main__":
    unittest.main()