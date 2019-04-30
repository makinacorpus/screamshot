[![Build Status](https://travis-ci.org/makinacorpus/screamshot.svg?branch=master)](https://travis-ci.org/makinacorpus/screamshot)
[![Coverage Status](https://coveralls.io/repos/github/makinacorpus/screamshot/badge.svg?branch=master&service=github)](https://coveralls.io/github/makinacorpus/screamshot?branch=master&service=github)
[![Documentation Status](https://readthedocs.org/projects/screamshot/badge/?version=latest)](https://screamshot.readthedocs.io/en/latest/?badge=latest)

# Screamshot
Python library to capture screenshots of web applications

## Good practices

* Any code addition must be done in your own branch. You can name it `fl/what_this_branch_brings` where 'f' is the first letter of your first name and 'l' the first letter of your last name.
* A branch resolves a specific issue.
* Please write exhaustive tests. The coverage must not decrease.
* Please merge the master branch into yours, run the tests and checks and correct all errors and warnings before pushing your code.
* When you think you have finished you can make a pull request.

## Testing and checks
### To start the tests and checks
#### The first time

1. Install **docker** and **docker-compose**.
2. Run: `docker-compose build`, to create all the required images.
3. To start the verification, run: `docker-compose up`.

#### When it is already setup

You just need to run `docker-compose up`.

#### To clean up

* If you want to stop containers and remove containers, networks, volumes, and images created by up command, run: `docker-compose down`.
* If you want to delete all the images, run: `docker rmi -f $(docker images -q)`.

### To write new tests

* You must use the `unittest` package
* You must put your test file in the **tests** folder
* You must name your test file using the following next pattern: **test_*.py**

#### Local server

A server with a web page can be used at the following address: <http://server:5000/index.html> and <http://server:5000/other.html>

## Usage
### Documentation

The documentation is accessible [here](https://screamshot.readthedocs.io/en/latest/), on readthedocs.


### Exemple with django

The server must be launched using --nothreading and --noreload as argument.
```
# views.py in a Django project
from django.http import HttpResponse

import asyncio

from screamshot import generate_bytes_img_prom

def home(request):
    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    asyncio.ensure_future(
        generate_bytes_img_prom('https://www.google.fr', future))
    loop.run_until_complete(future)

    return HttpResponse(future.result(), content_type='image')
``` 
Or using the already wrapped function
```
# views.py in a Django project
from django.http import HttpResponse

from screamshot import generate_bytes_img__django_wrap

def home(request):
    img = generate_bytes_img__django_wrap('https://www.google.fr')
    return HttpResponse(img, content_type='image')
``` 


#### Using Gunicorn

With [Gunicorn](https://gunicorn.org/) there isn't the thread related problems so we don't need to use the --nothreading and --noreload arguments.
