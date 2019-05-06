#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Meta data for screamshot."""


__author__ = """Maxime Courtet & Félix Cloup"""
__version__ = "0.1.9"


from screamshot.generate_bytes_img_functions import (
    generate_bytes_img,
    generate_bytes_img_prom,
    generate_bytes_img_django_wrap,
)


__all__ = [
    "generate_bytes_img",
    "generate_bytes_img_prom",
    "generate_bytes_img_django_wrap",
]
