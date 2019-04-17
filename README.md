# screamshot
Python library to capture screenshots of web applications

# Tests
1. If you want to run the tests in a MacOS environment, use the following command at the root of the project: `export PYTHONPATH=$PYTHONPATH:.`, 
2. `python3 -m unittest tests/generate_bytes_img_function_tests.py -v` runs all the tests of generate_bytes_img

# Usage
## generate_bytes_img_function_tests
### Description

If you want to access the documentation run: `python3 -m http.server` at the root of the project and go to <http://0.0.0.0:8000/doc/html/screamshot.html>

### Exemple

```
# views.py in a Django project
import asyncio

from django.http import HttpResponse

from screamshot import generate_bytes_img_prom


def home(request):
    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    asyncio.ensure_future(
        generate_bytes_img_prom('https://www.google.fr', future))
    loop.run_until_complete(future)

    print(futur.result())
    return HttpResponse('Done')
``` 
