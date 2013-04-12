#!/usr/bin/env python

from nose.tools import raises
import imp
import json
import os
import pickle
import sys

aur = imp.load_source("aur", os.path.join(os.path.dirname(__file__), "../aur.py"))
a = aur.AURClient()

def relative(path):
    return os.path.join(os.path.dirname(__file__), path)

@raises(aur.QueryTooShortError)
def testTooShort():
    with open(relative("samples/search/too-short")) as f:
        res = json.load(f)
        list(a.parseAURSearch(res, "search"))

@raises(aur.UnknownAURError)
def testBogusError():
    with open(relative("samples/search/bogus-error")) as f:
        res = json.load(f)
        list(a.parseAURSearch(res, "search"))

@raises(aur.UnexpectedResponseTypeError)
def testBogusReplyType():
    with open(relative("samples/search/unknown-type")) as f:
        res = json.load(f)
        list(a.parseAURSearch(res, "search"))

def testRealPackage():
    """
    >>> import aur, pickle, sys
    >>> a = aur.AURClient()
    >>> major = sys.version_info[0]
    >>> pickle.dump(list(a.search("yturl")), open("tests/samples/search/yturl-pickled-%d" % major, "wb+"))
    """

    with open(relative("samples/search/yturl-json")) as f:
        res = json.load(f)
        data = list(a.parseAURSearch(res, "search"))
        major = sys.version_info[0]
        assert data == pickle.load(open(relative("samples/search/yturl-pickled-%d" % major), "rb"))
