"""
This script installs the screamshot package and then waits for the server to respond to \
    <http://127.0.0.1:5000/index.html>. Then, it performs the MYPY and PYLINT checks as well as \
        the tests. Finally, it sends a closing request to the server and waits for it.
"""
#!/usr/bin/env python
from logging import getLogger, INFO
from subprocess import run
from argparse import ArgumentParser
from re import search

from screamshot.utils import wait_server_start, wait_server_close


logger = getLogger()
logger.setLevel(INFO)


def _parse_arg():
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--wait-url',
                        help='The URL to wait before starting the tests and checks',
                        type=str, default='http://127.0.0.1:5000/index.html')
    parser.add_argument('--close-url',
                        help='The URL that shutdown the server',
                        type=str, default='http://127.0.0.1:5000/close')
    return parser.parse_args()


def _parse_unittest_stdout(returncode, o_stdout):
    if returncode == 1:
        stdout = search(r'(?P<message>[^<]+FAILED)', o_stdout).group('message')
    else:
        stdout = search(r'(?P<message>[^<]+OK)', o_stdout).group('message')
    return stdout


def main():
    args = _parse_arg()
    exit_code = 0

    logger.info('\n####################\n     WAIT SERVER     \n####################\n')
    wait_server_start(args.wait_url, 'Waits for the connection since: %ds',
                      'Connection is available after: %ds')

    if not exit_code:
        logger.info('\n####################\n      UNITTEST      \n####################\n')
        pytest_res = run(["pytest", "-v", "--disable-warnings", "--cov=screamshot",
                          "--cov-report=term-missing"])
        exit_code = pytest_res.returncode

    if not exit_code:
        logger.info('\n####################\n       PYLINT       \n####################\n')
        pylint_res = run(['pylint', './screamshot'])
        exit_code = pylint_res.returncode

    if not exit_code:
        logger.info('\n####################\n        MYPY        \n####################\n')
        mypy_res = run(['mypy', '.'])
        exit_code = mypy_res.returncode

    logger.info('\n####################\n   SHUTDOWN SERVER   \n####################\n')
    wait_server_close(args.close_url, 'Waits for server since: %ds',
                      'Server shutdown after: %ds')

    exit(exit_code)


if __name__ == '__main__':
    main()
