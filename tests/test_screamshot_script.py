"""
Tests screamshot script
"""
from unittest import TestCase, main
from subprocess import run, PIPE
from os import remove


TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFraW5hIn0.\
jUTxi6c2-o3nHJ6Bq7zRXFoKixUyYetgPX3cToOayiA'


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

    def test_screamshot_username_without_password(self):
        res = run(['python3', 'screamshot/screamshot_script.py', '--no-sandbox',
                   '--username=makina', 'http://localhost:5000/protected_other',
                   'test_simple_screamshot.png'], stderr=PIPE)
        self.assertEqual(res.stderr.decode('utf-8'), 'A password must be specified\n')

    def test_screamshot_password_without_username(self):
        res = run(['python3', 'screamshot/screamshot_script.py', '--no-sandbox',
                   '--password=makina', 'http://localhost:5000/protected_other',
                   'test_simple_screamshot.png'], stderr=PIPE)
        self.assertEqual(res.stderr.decode('utf-8'), 'A username must be specified\n')

    def test_screamshot_with_username_and_password(self):
        """
        Takes a screenshot thanks to the script and checks if the image has been saved
        """
        with self.assertRaises(FileNotFoundError):
            open('test_simple_screamshot.png', 'r')
        run(['python3', 'screamshot/screamshot_script.py', '--no-sandbox', '--username=makina',
             '--password=makina', 'http://localhost:5000/other.html', 'test_simple_screamshot.png'])
        open('test_simple_screamshot.png', 'r')
        remove('test_simple_screamshot.png')

    def test_screamshot_with_bad_token(self):
        res = run(['python3', 'screamshot/screamshot_script.py', '--no-sandbox',
                   '--token=x!x', 'http://localhost:5000/protected_other',
                   'test_simple_screamshot.png'], stderr=PIPE)
        self.assertEqual(res.stderr.decode('utf-8'),
                         'Bad token argument, please read the documentation\n')

    def test_screamshot_with_token(self):
        """
        Takes a screenshot thanks to the script and checks if the image has been saved
        """
        with self.assertRaises(FileNotFoundError):
            open('test_simple_screamshot.png', 'r')
        run(['python3', 'screamshot/screamshot_script.py', '--no-sandbox',
             '--token=token:{0}'.format(TOKEN), 'http://localhost:5000/other.html',
             'test_simple_screamshot.png'])
        open('test_simple_screamshot.png', 'r')
        remove('test_simple_screamshot.png')


if __name__ == "__main__":
    main()
