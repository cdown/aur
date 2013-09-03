#!/usr/bin/env python

from nose.tools import raises
import aur
import json
import os
import sys


def relative(path):
    return os.path.join(os.path.dirname(__file__), path)


@raises(aur.exceptions.QueryTooShortError)
def test_query_too_short():
    with open(relative("samples/search/too-short")) as f:
        res = json.load(f)
        list(aur.query._parse_multi(res, "search"))


@raises(aur.exceptions.UnknownAURError)
def test_bogus_error():
    with open(relative("samples/search/bogus-error")) as f:
        res = json.load(f)
        list(aur.query._parse_multi(res, "search"))


@raises(aur.exceptions.UnexpectedResponseTypeError)
def test_bogus_reply_type():
    with open(relative("samples/search/unknown-type")) as f:
        res = json.load(f)
        list(aur.query._parse_multi(res, "search"))
