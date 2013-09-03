#!/usr/bin/env python

import aur


def test_search():
    assert len(list(aur.search("python2"))) > 50


def test_msearch():
    assert len(list(aur.msearch("cdown"))) > 1


def test_info():
    assert aur.info("yturl")
    assert aur.info(68930)


def test_multiinfo():
    assert len(list(aur.multiinfo(("yturl")))) == 1
    assert len(list(aur.multiinfo(("yturl", "yturl")))) == 1
    assert len(list(aur.multiinfo(("yturl", "yturl-git")))) == 2
    assert len(
        list(aur.multiinfo(("yturl", "yturl-git", "100-percent-nonexistent")))
    ) == 2
