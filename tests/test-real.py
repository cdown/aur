#!/usr/bin/env python

import aur


a = aur.AURClient()


def test_search():
    assert len(list(a.search("python2"))) > 50


def test_msearch():
    assert len(list(a.msearch("cdown"))) > 1


def test_info():
    assert a.info("yturl")
    assert a.info(68930)


def test_multiinfo():
    assert len(list(a.multiinfo(("yturl")))) == 1
    assert len(list(a.multiinfo(("yturl", "yturl")))) == 1
    assert len(list(a.multiinfo(("yturl", "yturl-git")))) == 2
    assert len(
        list(a.multiinfo(("yturl", "yturl-git", "100-percent-nonexistent")))
    ) == 2
