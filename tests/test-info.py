#!/usr/bin/env python

from nose.tools import raises
import aur
import json
import os
import pickle
import sys

a = aur.AURClient()

def relative(path):
    return os.path.join(os.path.dirname(__file__), path)

def testRealPackage():
    """
    curl -o tests/samples/info/yturl-json 'https://aur.archlinux.org/rpc.php?type=info&arg=yturl'

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
