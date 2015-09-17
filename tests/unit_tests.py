#!/usr/bin/env python

import calendar
import types
import json
import os
import aur
import httpretty
import re
from nose_parameterized import parameterized
from nose.tools import eq_ as eq


SAMPLE_DIR = os.path.join(os.path.dirname(__file__), 'samples')

@parameterized([
    'msearch_found',
    'msearch_not_found',
    'multiinfo_found',
    'multiinfo_not_found',
    'multiinfo_only_partial_found',
    'search_found',
    'search_not_found',
])
@httpretty.activate
def test_api_methods(test_file):
    method_name_to_test = test_file.split('_')[0]
    method_to_test = getattr(aur, method_name_to_test)

    api_resp_file = test_file + '.api_response'
    expected_file = test_file + '.expected'

    with open(os.path.join(SAMPLE_DIR, api_resp_file)) as resp_f:
        api_resp = resp_f.read()
    with open(os.path.join(SAMPLE_DIR, expected_file)) as expected_f:
        expected = json.load(expected_f)

    uri_regex = re.compile(r'/rpc\.php')
    httpretty.register_uri(
        httpretty.GET, uri_regex,
        body=api_resp, content_type='application/json',
    )

    got = method_to_test('hunter2')
    if isinstance(got, types.GeneratorType):
        # We need to compare the data, not the generator itself, so run it.
        got = [vars(package) for package in got]
    else:
        got = vars(got)

    for key in aur.KEYS_TO_CONVERT_TO_DATETIMES:
        # We store these in JSON as epochs, so convert them here
        if isinstance(got, list):
            for package in got:
                package[key] = calendar.timegm(package[key].timetuple())
        else:
            got[key] = calendar.timegm(got[key].timetuple())

    eq(got, expected)
