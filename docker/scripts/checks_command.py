"""
This script waits for the server to respond to <http://server:5000/index.html>, and then \
    performs the MYPY and PYLINT checks. Finally he performs the unittests.
"""
#!/usr/bin/env python
import os
import logging
from time import sleep
import subprocess
import re
from urllib3.exceptions import MaxRetryError

from requests import get
from requests.exceptions import ConnectionError as RequestsConnectionError


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


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


def main():
    _wait_server('http://server:5000/index.html', 'Waits for the connection since: %ds',
                 'Connection is available after: %ds')
    logger.info('\n####################\n        MYPY        \n####################\n')
    os.system('mypy .')
    logger.info('\n####################\n      UNITTEST      \n####################\n')
    res = subprocess.run(["python3", "-m", "unittest",
                          "tests/generate_bytes_img_function_tests.py", "-v"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = res.stderr.decode('utf8')
    if res.returncode == 1:
        stdout = re.search(r'(?P<message>[^<]+FAILED)', stderr).group('message')
    else:
        stdout = re.search(r'(?P<message>[^<]+OK)', stderr).group('message')
    logger.info(stdout)
    _wait_server('http://server:5000/close', 'Waits for server since: %ds',
                 'Server shutdown after: %ds')


if __name__ == '__main__':
    main()
