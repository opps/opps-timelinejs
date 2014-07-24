#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources


pkg_resources.declare_namespace(__name__)

VERSION = (0, 1, 1)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = u"Timeline JS App for Opps CMS"

__author__ = u"Abdallah Deeb <abdallah@deeb.me> / Bruno Cezar Rocha"
__credits__ = []
__email__ = u"rochacbruno@gmail.com"
__license__ = u"MLP License"
