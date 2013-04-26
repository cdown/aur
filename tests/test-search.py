#!/usr/bin/env python

from nose.tools import raises
import aur
import json
import os
import sys

a = aur.AURClient()

def relative(path):
    return os.path.join(os.path.dirname(__file__), path)

@raises(aur.exceptions.QueryTooShortError)
def testTooShort():
    with open(relative("samples/search/too-short")) as f:
        res = json.load(f)
        list(a.parseAURSearch(res, "search"))

@raises(aur.exceptions.UnknownAURError)
def testBogusError():
    with open(relative("samples/search/bogus-error")) as f:
        res = json.load(f)
        list(a.parseAURSearch(res, "search"))

@raises(aur.exceptions.UnexpectedResponseTypeError)
def testBogusReplyType():
    with open(relative("samples/search/unknown-type")) as f:
        res = json.load(f)
        list(a.parseAURSearch(res, "search"))
