.. Screamshot documentation master file, created by
   sphinx-quickstart on Thu Apr 25 17:19:06 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Screamshot's documentation
==========================

Screamshot_ is a python library to capture screenshots of web pages.

.. _Screamshot: https://github.com/makinacorpus/screamshot/

Specification
-------------

It is based on the Pyppeteer_ library that uses the Asyncio_ package and therefore **asynchronous funcrions**. Thus, you may experience some thread issues.

.. _Pyppeteer: https://github.com/miyakogi/pyppeteer/
.. _Asyncio: https://docs.python.org/3/library/asyncio.html

Installation
------------

Screamshot requires **Python 3.5** or more.

Install by pip from PyPI:

``pip install screamshot``

Usage
-----

**Exemple:** a Django_ view that uses screamshot

.. code-block:: Python

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


In this case, if you use ``manage.py``, the server must be launched using ``--nothreading`` and ``--noreload`` as argument.

.. _Django: https://www.djangoproject.com

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* `Screamshot module`_
* :ref:`search`

.. _`Screamshot module`: screamshot.html
