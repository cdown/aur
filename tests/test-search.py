#!/usr/bin/env python

from nose.tools import raises, eq_ as eq
import datetime
import aur
import os
import requests_mock


def relative(path):
    return os.path.join(os.path.dirname(__file__), path)


@requests_mock.mock()
@raises(aur.QueryTooShortError)
def test_query_too_short(rq_mock):
    with open(relative('samples/search/too-short')) as mock_f:
        rq_mock.get(requests_mock.ANY, text=mock_f.read())
        list(aur.search('xxxxx'))


@requests_mock.mock()
@raises(aur.UnknownAURError)
def test_bogus_error(rq_mock):
    with open(relative('samples/search/bogus-error')) as mock_f:
        rq_mock.get(requests_mock.ANY, text=mock_f.read())
        list(aur.msearch('xxxxx'))


@requests_mock.mock()
def test_search(rq_mock):
    with open(relative('samples/search/search')) as mock_f:
        rq_mock.get(requests_mock.ANY, text=mock_f.read())

        results = list(aur.search('yturl'))

        eq(len(results), 2)
        eq(
            results[0].__dict__,
            {
                'url_path': '/packages/yt/yturl-git/yturl-git.tar.gz',
                'first_submitted': datetime.datetime(2012, 5, 11, 22, 7, 42),
                'id': 59216,
                'name': 'yturl-git',
                'category_id': 12,
                'version': '20140312033836.ba8983c-1',
                'last_modified': datetime.datetime(2014, 3, 12, 4, 34, 28),
                'out_of_date': False,
                'description': 'Print direct URLs to YouTube videos.',
                'license': ' MIT ',
                'maintainer': 'cdown',
                'url': 'http://github.com/cdown/yturl',
                'num_votes': 11,
                'package_base': 'yturl-git',
                'package_base_id': 59216,
            }
        )
        eq(
            results[1].__dict__,
            {
                'license': ' MIT ',
                'url': 'http://github.com/cdown/yturl',
                'out_of_date': False,
                'description': 'Print direct URLs to YouTube videos.',
                'version': '1.16-1',
                'num_votes': 1,
                'id': 68930,
                'url_path': '/packages/yt/yturl/yturl.tar.gz',
                'maintainer': 'cdown',
                'name': 'yturl',
                'first_submitted': datetime.datetime(2013, 4, 8, 13, 16, 36),
                'category_id': 12,
                'last_modified': datetime.datetime(2014, 3, 12, 4, 33, 59),
                'package_base': 'yturl',
                'package_base_id': 68930,
            }
        )

@requests_mock.mock()
def test_msearch(rq_mock):
    with open(relative('samples/search/msearch')) as mock_f:
        rq_mock.get(requests_mock.ANY, text=mock_f.read())

        results = list(aur.msearch('cdown'))

        eq(len(results), 2)
        eq(
            results[0].__dict__,
            {
                'id': 59216,
                'name': 'yturl-git',
                'url': 'http://github.com/cdown/yturl',
                'description': 'Print direct URLs to YouTube videos.',
                'category_id': 12,
                'version': '20140312033836.ba8983c-1',
                'out_of_date': False,
                'num_votes': 11,
                'first_submitted': datetime.datetime(2012, 5, 11, 22, 7, 42),
                'last_modified': datetime.datetime(2014, 3, 12, 4, 34, 28),
                'maintainer': 'cdown',
                'license': ' MIT ',
                'url_path': '/packages/yt/yturl-git/yturl-git.tar.gz',
                'package_base': 'yturl-git',
                'package_base_id': 59216,
            }
        )
        eq(
            results[1].__dict__,
            {
                'maintainer': 'cdown',
                'url': 'http://github.com/cdown/yturl',
                'last_modified': datetime.datetime(2014, 3, 12, 4, 33, 59),
                'description': 'Print direct URLs to YouTube videos.',
                'license': ' MIT ',
                'name': 'yturl',
                'num_votes': 1,
                'id': 68930,
                'url_path': '/packages/yt/yturl/yturl.tar.gz',
                'out_of_date': False,
                'version': '1.16-1',
                'category_id': 12,
                'first_submitted': datetime.datetime(2013, 4, 8, 13, 16, 36),
                'package_base': 'yturl',
                'package_base_id': 68930,
            }
        )

@requests_mock.mock()
def test_info(rq_mock):
    with open(relative('samples/search/multiinfo')) as mock_f:
        rq_mock.get(requests_mock.ANY, text=mock_f.read())

        result = aur.info('cdown')

        eq(
            result.__dict__,
            {
                'version': '1.6.0-2',
                'first_submitted': datetime.datetime(2006, 11, 8, 7, 37, 11),
                'description': 'CUPS driver for Konica Minolta magicolor 2430 Desklaser printer',
                'url_path': '/packages/cu/cups-mc2430dl/cups-mc2430dl.tar.gz',
                'num_votes': 3,
                'url': 'http://konicaminolta.com/',
                'out_of_date': False,
                'license': 'GPL',
                'last_modified': datetime.datetime(2012, 8, 7, 15, 41, 13),
                'id': 7451,
                'name': 'cups-mc2430dl',
                'category_id': 14,
                'maintainer': 'frigg',
                'package_base': 'cups-mc2430dl',
                'package_base_id': 7451,
            },
        )

@requests_mock.mock()
def test_multiinfo(rq_mock):
    with open(relative('samples/search/multiinfo')) as mock_f:
        rq_mock.get(requests_mock.ANY, text=mock_f.read())

        results = list(aur.multiinfo('cdown'))

        eq(len(results), 2)
        eq(
            results[0].__dict__,
            {
                'version': '1.6.0-2',
                'first_submitted': datetime.datetime(2006, 11, 8, 7, 37, 11),
                'description': 'CUPS driver for Konica Minolta magicolor 2430 Desklaser printer',
                'url_path': '/packages/cu/cups-mc2430dl/cups-mc2430dl.tar.gz',
                'num_votes': 3,
                'url': 'http://konicaminolta.com/',
                'out_of_date': False,
                'license': 'GPL',
                'last_modified': datetime.datetime(2012, 8, 7, 15, 41, 13),
                'id': 7451,
                'name': 'cups-mc2430dl',
                'category_id': 14,
                'maintainer': 'frigg',
                'package_base': 'cups-mc2430dl',
                'package_base_id': 7451,
            },
        )
        eq(
            results[1].__dict__,
            {
                'version': '2008.01.23-1',
                'name': 'cups-xerox',
                'license': 'custom',
                'category_id': 14,
                'out_of_date': False,
                'maintainer': 'niq000',
                'url': 'http://www.support.xerox.com/go/getfile.asp?objid=61334',
                'url_path': '/packages/cu/cups-xerox/cups-xerox.tar.gz',
                'first_submitted': datetime.datetime(2006, 9, 27, 21, 10, 36),
                'id': 153503,
                'description': 'Drivers for various Xerox printers',
                'num_votes': 21,
                'last_modified': datetime.datetime(2015, 2, 19, 23, 35, 16),
                'package_base': 'cups-xerox',
                'package_base_id': 6941,
            },
        )
