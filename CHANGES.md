CHANGELOG
=========

0.0.1
===

Initialization of Screamshot library
1. __init__ file:
    * __author__
    * __version__
    * __all__
2. core file:
    * A `ScreenShot` object with three methods:
        * `load`, loads a web page
        * `screamshot`, takes a screenshot of a loaded page
        * `load_and_screamshot`, loads a web page and takes a screenshot

0.1.0
===

There is no more `ScreenShot` object just a function named `generate_bytes_img` which
takes some parameters and returns a binary `bytes` object.

0.1.1
===

`generate_bytes_img` is no more a sync function and `generate_bytes_img_prom` has been added
`generate_bytes_img_prom` uses the `asyncio.Future` object

0.1.2
===

A test and verification tool using Docker is now available

0.1.3
===

Add two commands:
* `browser-manager`
* `screamshot`

0.1.4
===

Add two functions:
* `serialize`
* `deserialize`

0.1.5
===

Add `generate_bytes_img_django_wrap` function
