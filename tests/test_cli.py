from contextlib import redirect_stdout
import io
import unittest

from defect_detection import __version__
from defect_detection.cli import main


class CliTests(unittest.TestCase):
    def test_version_command(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["version"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), __version__)


if __name__ == "__main__":
    unittest.main()

