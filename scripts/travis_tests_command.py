"""
This script waits for the server to respond to <http://127.0.0.1:5000/index.html>. Then runs \
    the tests and finaly sends a closing request to the server and waits for it.
"""
from os import system
from subprocess import run
from logging import getLogger, DEBUG
from argparse import ArgumentParser

from screamshot.utils import wait_server


logger = getLogger()
logger.setLevel(DEBUG)


def _parse_arg():
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--wait-url',
                        help='The URL to wait before starting the tests and checks',
                        type=str, default='http://127.0.0.1:5000/index.html')
    return parser.parse_args()


def main():
    args = _parse_arg()

    logger.info('\n####################\n     WAIT SERVER     \n####################\n')
    wait_server(args.wait_url, 'Waits for the connection since: %ds',
                'Connection is available after: %ds')
    logger.info('\n####################\n   LAUNCH BROWSER   \n####################\n')
    system('browser-manager -o -ns')

    logger.info('\n####################\n      UNITTEST      \n####################\n')
    unittest_res = run(["python3", "-m", "unittest"])

    logger.info('\n####################\n    CLOSE BROWSER  \n####################\n')
    system('browser-manager -c')

    exit(unittest_res.returncode)


if __name__ == '__main__':
    main()
