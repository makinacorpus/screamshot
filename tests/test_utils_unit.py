"""
Unit tests of `utils.py` functions
"""
from os import remove
from unittest import TestCase, main
from unittest import mock

from urllib3.exceptions import MaxRetryError

from requests.exceptions import ConnectionError as RequestsConnectionError

from screamshot.utils import (_check_wait_until_arg, url_match, set_endpoint, FILENAME_ENDPOINT,
                              get_endpoint, wait_server_start, wait_server_close)

from _io import TextIOWrapper


class UnistTestsUtilsFunctions(TestCase):
    """
    Test class
    """
    def test_check_wait_until_arg(self):
        """
        Tests _check_wait_until_arg
        """
        self.assertTrue(_check_wait_until_arg('load'))
        self.assertTrue(_check_wait_until_arg(['load']))

        self.assertTrue(_check_wait_until_arg('domcontentloaded'))
        self.assertTrue(_check_wait_until_arg(['domcontentloaded']))

        self.assertTrue(_check_wait_until_arg('networkidle0'))
        self.assertTrue(_check_wait_until_arg(['networkidle0']))

        self.assertTrue(_check_wait_until_arg('networkidle2'))
        self.assertTrue(_check_wait_until_arg(['networkidle2']))

        self.assertFalse(_check_wait_until_arg('no'))
        self.assertFalse(_check_wait_until_arg(['no']))

    def test_url_match(self):
        """
        Tests url_match
        """
        self.assertTrue(url_match('https://www.google.fr', 'https://www.google.fr'))
        self.assertTrue(url_match('https://www.google.fr/', 'https://www.google.fr'))
        self.assertTrue(url_match('https://www.google.fr', 'https://www.google.fr/'))

        self.assertFalse(url_match('http://www.google.fr', 'https://www.google.fr'))
        self.assertFalse(url_match('http://www.google.fr/', 'https://www.google.fr'))
        self.assertFalse(url_match('http://www.google.fr', 'https://www.google.fr/'))

    def test_set_endpoint(self):
        """
        Tests set_endpoint
        """
        with self.assertRaises(FileNotFoundError):
            open(FILENAME_ENDPOINT, 'r')

        set_endpoint('toto')
        endpoint_f = open(FILENAME_ENDPOINT, 'r')
        self.assertTrue(isinstance(endpoint_f, TextIOWrapper))
        endpoint_fc = endpoint_f.readlines()
        self.assertEqual(len(endpoint_fc), 1)
        endpoint = endpoint_fc[0][:-1]
        self.assertEqual('toto', endpoint)

        endpoint_f.close()
        remove(FILENAME_ENDPOINT)

    def test_get_end_point(self):
        """
        Tests get_end_point
        """
        self.assertEqual(get_endpoint(), None)

        with self.assertLogs() as logs:
            get_endpoint()
        self.assertEqual(logs.output, ['WARNING:root:{0} not found'.format(FILENAME_ENDPOINT)])

        endpoint_f = open(FILENAME_ENDPOINT, 'w')
        endpoint_f.write('toto\n')
        endpoint_f.close()
        self.assertEqual(get_endpoint(), 'toto')

        remove(FILENAME_ENDPOINT)

    @mock.patch('screamshot.utils.get')
    def test_wait_server_start(self, mock_get):
        """
        Tests wait_server_start
        """
        mock_get.side_effect = MaxRetryError(None, 'http://false')
        with self.assertRaises(MaxRetryError):
            with self.assertLogs() as logs:
                wait_server_start('http://false', 'Wait for: %ds', '')
        self.assertEqual(logs.output, ['INFO:root:Wait for: 0s', 'INFO:root:Wait for: 1s',
                                       'INFO:root:Wait for: 2s', 'INFO:root:Wait for: 3s',
                                       'INFO:root:Wait for: 4s', 'INFO:root:Wait for: 5s',
                                       'INFO:root:Wait for: 6s', 'INFO:root:Wait for: 7s',
                                       'INFO:root:Wait for: 8s', 'INFO:root:Wait for: 9s'])

        mock_response = mock.Mock()
        mock_response.status_code.return_value = 200
        mock_get.side_effect = [MaxRetryError(None, 'http://false'), mock_response]
        with self.assertLogs() as logs:
            wait_server_start('http://false', 'Wait for: %ds', 'Awaited: %ds')
        self.assertEqual(logs.output, ['INFO:root:Wait for: 0s', 'INFO:root:Awaited: 1s'])

        mock_get.side_effect = mock_response
        with self.assertLogs() as logs:
            wait_server_start('http://false', 'Wait for: %ds', 'Awaited: %ds')
        self.assertEqual(logs.output, ['INFO:root:Awaited: 0s'])

    @mock.patch('screamshot.utils.get')
    def test_wait_server_close(self, mock_get):
        """
        Tests wait_server_close
        """
        mock_response = mock.Mock()
        mock_response.status_code.return_value = 200
        mock_get.side_effect = mock_response
        with self.assertRaises(MaxRetryError):
            with self.assertLogs() as logs:
                wait_server_close('http://false', 'Wait for: %ds', '')
        self.assertEqual(logs.output, ['INFO:root:Wait for: 0s', 'INFO:root:Wait for: 1s',
                                       'INFO:root:Wait for: 2s', 'INFO:root:Wait for: 3s',
                                       'INFO:root:Wait for: 4s', 'INFO:root:Wait for: 5s',
                                       'INFO:root:Wait for: 6s', 'INFO:root:Wait for: 7s',
                                       'INFO:root:Wait for: 8s', 'INFO:root:Wait for: 9s'])

        mock_response = mock.Mock()
        mock_response.status_code.return_value = 200
        mock_get.side_effect = [mock_response, RequestsConnectionError()]
        with self.assertLogs() as logs:
            wait_server_close('http://false', 'Wait for: %ds', 'Awaited: %ds')
        self.assertEqual(logs.output, ['INFO:root:Wait for: 0s', 'INFO:root:Awaited: 1s'])

        mock_get.side_effect = RequestsConnectionError()
        with self.assertLogs() as logs:
            wait_server_close('http://false', 'Wait for: %ds', 'Awaited: %ds')
        self.assertEqual(logs.output, ['INFO:root:Awaited: 0s'])


if __name__ == '__main__':
    main()
