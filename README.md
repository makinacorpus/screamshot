[![Build Status](https://travis-ci.org/makinacorpus/screamshot.svg?branch=master)](https://travis-ci.org/makinacorpus/screamshot)
[![Coverage Status](https://coveralls.io/repos/github/makinacorpus/screamshot/badge.svg?branch=master)](https://coveralls.io/github/makinacorpus/screamshot?branch=master&service=github)

# screamshot
Python library to capture screenshots of web applications

# Good practices before committing

Please run the tests and checks and correct all errors and warnings before committing.

# Testing and checks
## To start the tests and checks
### The first time

1. Install **Docker**
2. Run: `docker-compose build`, to create all the required images
3. To start the verification, run: `docker-compose up`

### When it is already setup

You just need to run `docker-compose up`.

### To clean up

* If you want to stop containers and remove containers, networks, volumes, and images created by up, run: `docker-compose down`.
* If you want to delete all the images, run: `docker --rmi all`.

## To write new tests

* You must use the `unittest` package
* You must put your test file in the **tests** folder
* You must name your test file using the following next pattern: **tests_*.py**

### Local server

A server with a web page can be used at the following address: <http://server:5000/index.html>

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

    print(future.result())
    return HttpResponse('Done')
``` 
