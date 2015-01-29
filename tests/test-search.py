#!/usr/bin/env python

from nose.tools import raises, eq_ as eq
import datetime
import aur
import json
import os
import sys
from mock import patch


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

@patch('aur.query._query_api')
def test_search(qa_mock):
    qa_mock.return_value = {
        u'resultcount': 2,
        u'results': [
            {
                u'CategoryID': 12,
                u'Description': u'Print direct URLs to YouTube videos.',
                u'FirstSubmitted': 1336774062,
                u'ID': 59216,
                u'LastModified': 1394598868,
                u'License': u' MIT ',
                u'Maintainer': u'cdown',
                u'Name': u'yturl-git',
                u'NumVotes': 14,
                u'OutOfDate': 0,
                u'PackageBase': u'yturl-git',
                u'PackageBaseID': 59216,
                u'URL': u'http://github.com/cdown/yturl',
                u'URLPath': u'/packages/yt/yturl-git/yturl-git.tar.gz',
                u'Version': u'20140312033836.ba8983c-1'
            },
        ],
        u'type': u'search',
        u'version': 1
    }

    results = list(aur.search('xxxxx'))

    eq(
        {'category_id': 12, 'maintainer': u'cdown', 'name': u'yturl-git', 'license': u' MIT ', 'url': u'http://github.com/cdown/yturl', 'first_submitted': datetime.datetime(2012, 5, 11, 22, 7, 42), 'version': u'20140312033836.ba8983c-1', 'last_modified': datetime.datetime(2014, 3, 12, 4, 34, 28), 'num_votes': 14, 'out_of_date': False, 'url_path': u'/packages/yt/yturl-git/yturl-git.tar.gz', 'id': 59216, 'description': u'Print direct URLs to YouTube videos.'},
        results[0].__dict__
    )
