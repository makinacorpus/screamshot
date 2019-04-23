"""
This script waits for the server to respond to <http://server:5000/index.html>, and then \
    performs the MYPY and PYLINT checks and the unittests. Finally it sends a closing request \
        to the server and waits for it

"""
#!/usr/bin/env python
import os
import logging
from time import sleep
import subprocess
from re import search
from argparse import ArgumentParser

from urllib3.exceptions import MaxRetryError

from requests import get
from requests.exceptions import ConnectionError as RequestsConnectionError


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def _parse_arg():
    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--wait-url',
                        help='The URL to wait before starting the tests and checks',
                        type=str, default='http://127.0.0.1:5000/index.html')
    parser.add_argument('--close-url',
                        help='The URL that shutdown the server',
                        type=str, default='http://127.0.0.1:5000/close')
    parser.add_argument('--no-mypy',
                        help='Mypy checks will not be run', action='store_true', default=False)
    parser.add_argument('--no-pylint',
                        help='Pylint checks will not be run', action='store_true', default=False)
    parser.add_argument('--no-unittest-parsing',
                        help='By default, unittest stdout is parsed to remove unnecessary warnings',
                        action='store_true', default=False)
    parser.add_argument('--no-server-closing',
                        help='By default, it closes the server',
                        action='store_true', default=False)

    return parser.parse_args()


def _wait_server(url, waiting_message, final_message):
    count = 0
    server_started = False
    while not server_started:
        try:
            get(url)
            server_started = True
        except (RequestsConnectionError, MaxRetryError) as _:
            sleep(1)
            logger.info(waiting_message, count)
            count += 1
    logger.info(final_message, count)


def _parse_unittest_stdout(returncode, o_stdout):
    if returncode == 1:
        stdout = search(r'(?P<message>[^<]+FAILED)', o_stdout).group('message')
    else:
        stdout = search(r'(?P<message>[^<]+OK)', o_stdout).group('message')
    return stdout


def main():
    args = _parse_arg()

    logger.info('\n####################\n    SETUP INSTALL   \n####################\n')
    os.system('sudo python3 setup.py install')

    logger.info('\n####################\n     WAIT SERVER     \n####################\n')
    _wait_server(args.wait_url, 'Waits for the connection since: %ds',
                 'Connection is available after: %ds')

    logger.info('\n####################\n   LAUNCH BROWSER   \n####################\n')
    os.system('browser-manager -o -ns')

    logger.info('\n####################\n      UNITTEST      \n####################\n')
    unittest_res = subprocess.run(["python3", "-m", "unittest"],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = unittest_res.stderr.decode('utf8')
    if not args.no_unittest_parsing:
        # Pyppeteer sends many warnings when closing Python
        # The following lines erase them
        stdout = _parse_unittest_stdout(unittest_res.returncode, stderr)
        logger.info(stdout)
    else:
        logger.info(stderr)
    if unittest_res.returncode:
        logger.info('\n####################\n   SHUTDOWN SERVER   \n####################\n')
        _wait_server(args.close_url, 'Waits for server since: %ds',
                     'Server shutdown after: %ds')
        logger.info('\n####################\n    CLOSE BROWSER  \n####################\n')
        os.system('browser-manager -c')
        exit(1)

    logger.info('\n####################\n    CLOSE BROWSER  \n####################\n')
    os.system('browser-manager -c')

    if not args.no_pylint:
        logger.info('\n####################\n       PYLINT       \n####################\n')
        pylint_res = subprocess.run(['pylint', './screamshot'])
        if pylint_res.returncode:
            logger.info('\n####################\n   SHUTDOWN SERVER   \n####################\n')
            _wait_server(args.close_url, 'Waits for server since: %ds',
                         'Server shutdown after: %ds')
            exit(1)

    if not args.no_mypy:
        logger.info('\n####################\n        MYPY        \n####################\n')
        mypy_res = subprocess.run(['mypy', '.'])
        if mypy_res.returncode:
            logger.info('\n####################\n   SHUTDOWN SERVER   \n####################\n')
            _wait_server(args.close_url, 'Waits for server since: %ds',
                         'Server shutdown after: %ds')
            exit(1)

    if not args.no_server_closing:
        logger.info('\n####################\n   SHUTDOWN SERVER   \n####################\n')
        _wait_server(args.close_url, 'Waits for server since: %ds',
                     'Server shutdown after: %ds')
    exit(unittest_res.returncode)


if __name__ == '__main__':
    main()
