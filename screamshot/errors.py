"""
Screamshot exceptions
"""
class ScreamshotException(Exception):
    """
    Base screamshot exception
    """


class BadUrl(ScreamshotException):
    """
    Bad url excpetion
    """


class BadSelector(ScreamshotException):
    """
    Selector exception
    """
