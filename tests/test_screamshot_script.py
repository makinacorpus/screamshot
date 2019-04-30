"""
Tests screamshot script
"""
from unittest import TestCase, main
from subprocess import run
from os import remove


class TestScreamshotScript(TestCase):
    """
    Test class
    """

    def test_simple_screamshot(self):
        """
        Takes a screenshot thanks to the script and checks if the image has been saved
        """
        with self.assertRaises(FileNotFoundError):
            open("test_simple_screamshot.png", "r")
        run(
            [
                "python3",
                "screamshot/screamshot_script.py",
                "--no-sandbox",
                "http://localhost:5000/index.html",
                "test_simple_screamshot.png",
            ]
        )
        open("test_simple_screamshot.png", "r")
        remove("test_simple_screamshot.png")


if __name__ == "__main__":
    main()
