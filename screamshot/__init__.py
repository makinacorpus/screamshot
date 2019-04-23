"""
Python library to capture screenshots of web pages
"""


__author__ = """Maxime Courtet & Félix Cloup"""
__version__ = "0.1.2"


from screamshot.utils import to_sync, get_browser, get_browser_sync, goto_page, goto_page_sync
from screamshot.generate_bytes_img import generate_bytes_img, generate_bytes_img_prom


__all__ = ['generate_bytes_img', 'generate_bytes_img_prom', "to_sync",
           "get_browser", "get_browser_sync", "goto_page", "goto_page_sync"]
