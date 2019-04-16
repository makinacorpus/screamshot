=========
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
takes some parameters and returns a base64 `bytes` object.
