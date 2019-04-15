# screamshot
Python library to capture screenshots of web applications

# Tests
1. If you want to run the tests in a MacOS environment, use the following command at the root of the project: `export PYTHONPATH=$PYTHONPATH:.`, 
2. `python3 -m unittest tests/generate_bytes_img_function_tests.py` runs all the tests of generate_bytes_img

# Usage
## generate_bytes_img_function_tests
### Description

This function takes the following parameters and returns a base64 `bytes` object:
* url: mandatory, str, the website's url
* check_params: optionnal, bool, default True, allows the verification of parameters
* width: optionnal, int, the window's width
* height: optionnal, int, the window's height
* selector: optionnal, str, CSS3 selector, item whose screenshot is taken
* wait_for: optionnal, str, CSS3 selector, item to wait before taking the screenshot
* wait_until: optionnal, str, define how long you wait for the page to be loaded should be
  either load, domcontentloaded, networkidle0 or networkidle2

### Precision

If `check_params` is equal to `True` and if a parameter does not respect the conditions,
the function raises an `AssertionError`

### Warning

It uses pyppeteer and so async functions
