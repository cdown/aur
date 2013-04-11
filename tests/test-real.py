#!/usr/bin/env python

import imp
import os

aur = imp.load_source("aur", os.path.join(os.path.dirname(__file__), "../aur.py"))
a = aur.AURClient()

def testSearch():
    assert len(list(a.search("python2"))) > 50

def testMSearch():
    assert len(list(a.msearch("cdown"))) > 1

def testInfo():
    assert a.info("yturl")
    assert a.info(68930)
