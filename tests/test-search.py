#!/usr/bin/env python

from nose.tools import raises
import imp
import json
import os

aur = imp.load_source("aur", os.path.join(os.path.dirname(__file__), "../aur.py"))
a = aur.AURClient()

def relative(path):
    return os.path.join(os.path.dirname(__file__), path)

@raises(aur.QueryTooShortError)
def testTooShort():
    with open(relative("samples/search/too-short")) as f:
        res = json.load(f)
        list(a.parseSearch(res))
