"""
Unit tests of `generate_bytes_img_function.py`
"""
from unittest import TestCase, main

from screamshot.generate_bytes_img import _parse_parameters


class TestGenerateBytesImgFunctionUnit(TestCase):
    """
    Test class
    """
    def test_parse_parameters(self):
        """
        Tests _parse_parameters
        """
        self.assertEqual(_parse_parameters(),
                         {'path': None, 'arg_viewport': {}, 'full_page': False, 'selector': None,
                          'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(width=800),
                         {'path': None, 'arg_viewport': {'width': 800}, 'full_page': False,
                          'selector': None, 'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(height=800),
                         {'path': None, 'arg_viewport': {'height': 800}, 'full_page': False,
                          'selector': None, 'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(wait_until=['networkidle0']),
                         {'path': None, 'arg_viewport': {}, 'full_page': False, 'selector': None,
                          'wait_for': None, 'wait_until': ['networkidle0']})
        self.assertEqual(_parse_parameters(wait_until='networkidle0'),
                         {'path': None, 'arg_viewport': {}, 'full_page': False, 'selector': None,
                          'wait_for': None, 'wait_until': ['networkidle0']})
        self.assertEqual(_parse_parameters(full_page=True),
                         {'path': None, 'arg_viewport': {}, 'full_page': True, 'selector': None,
                          'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(selector='div'),
                         {'path': None, 'arg_viewport': {}, 'full_page': False, 'selector': 'div',
                          'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(wait_for='div'),
                         {'path': None, 'arg_viewport': {}, 'full_page': False, 'selector': None,
                          'wait_for': 'div', 'wait_until': ['load']})


if __name__ == '__main__':
    main()
