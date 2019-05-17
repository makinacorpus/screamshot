"""
Screamshot exceptions
"""


class ScreamshotException(Exception):
    """
    Base screamshot exception
    """


class BadUrl(ScreamshotException):
    """
    Bad url exception
    """


class BadAuth(ScreamshotException):
    """
    Bad authentification exception
    """


class BadSelector(ScreamshotException):
    """
    Selector exception
    """
