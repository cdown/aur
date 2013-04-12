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

def testRealPackage():
    """
    >>> import aur, pickle, sys
    >>> a = aur.AURClient()
    >>> major = sys.version_info[0]
    >>> pickle.dump(a.info("yturl"), open("tests/samples/info/yturl-pickled-%d" % major, "wb+"))
    """

    with open(relative("samples/info/yturl-json")) as f:
        res = json.load(f)
        data = a.parseAURPackageInfo(res)
        major = sys.version_info[0]
        assert data == pickle.load(open(relative("samples/info/yturl-pickled-%d" % major), "rb"))
