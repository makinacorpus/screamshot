# screamshot
Python library to capture screenshots of web applications

# Tests
1. If you want to run the tests in a MacOS environment, use the following command at the root of the project: `export PYTHONPATH=$PYTHONPATH:.`, 
2. `python3 -m unittest tests/generate_bytes_img_function_tests.py` runs all the tests of generate_bytes_img

# Usage
## generate_bytes_img_function_tests
### Description

If you want to access the documentation run: `python3 -m http.server` at the root of the project and go to <http://0.0.0.0:8000/doc/html/screamshot.html>

### Exemple

```
from screamshot import generate_bytes_img


def main():
    img = generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                             selector='.image-right', wait_until='networkidle0')
    print(img)


if __name__ == '__main__':
    main()
``` 
