"""
Tests screamshot script
"""
from unittest import TestCase, main
from subprocess import run
from os import remove

from screamshot.utils import to_sync, open_browser, close_browser


class TestScreamshotScript(TestCase):
    """
    Test class
    """
    def setUp(self):
        to_sync(open_browser(True, launch_args=['--no-sandbox']))

    def test_simple_screamshot(self):
        """
        Takes a screenshot thanks to the script and checks if the image has been saved
        """
        run(['python3', 'screamshot/screamshot_script.py', 'http://localhost:5000/other.html',
             'test_simple_screamshot.png'])
        open('test_simple_screamshot.png', 'r')
        remove('test_simple_screamshot.png')

    def tearDown(self):
        to_sync(close_browser())


if __name__ == '__main__':
    main()
