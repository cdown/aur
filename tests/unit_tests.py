#!/usr/bin/env python

import calendar
import json
import types
import os
import aur
import httpretty
import re
from nose_parameterized import parameterized
from nose.tools import eq_ as eq, assert_raises
from hypothesis import given, assume
from hypothesis.strategies import integers, sampled_from, text, one_of, none


SAMPLE_DIR = os.path.join(os.path.dirname(__file__), 'samples')

@parameterized([
    'msearch_found',
    'msearch_not_found',
    'multiinfo_found',
    ('multiinfo_not_found', aur.MissingPackageError),
    ('multiinfo_only_partial_found', aur.MissingPackageError),
    'search_found',
    'search_not_found',
])
@httpretty.activate
def test_api_methods(test_file, should_raise_exc=None):
    method_name_to_test = test_file.split('_')[0]
    method_to_test = getattr(aur, method_name_to_test)

    api_resp_file = test_file + '.api_response'
    expected_file = test_file + '.expected'
    args_file = test_file + '.args'

    with open(os.path.join(SAMPLE_DIR, api_resp_file)) as resp_f:
        api_resp = resp_f.read()
    with open(os.path.join(SAMPLE_DIR, expected_file)) as expected_f:
        expected = json.load(expected_f)
    with open(os.path.join(SAMPLE_DIR, args_file)) as args_f:
        args = json.load(args_f)

    httpretty.register_uri(
        httpretty.GET, re.compile(r'/rpc\.php'),
        body=api_resp, content_type='application/json',
    )

    if should_raise_exc is not None:
        with assert_raises(should_raise_exc):
            method_to_test(args)
        return
    else:
        got = method_to_test(args)

    if isinstance(got, list) or isinstance(got, types.GeneratorType):
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


@given(sampled_from(x for x in aur.CATEGORIES if x is not None))
def test_category_name_to_id(category_name):
    eq(
        aur.category_name_to_id(category_name),
        aur.CATEGORIES.index(category_name),
    )


@given(one_of(text(), none()))
def test_category_name_to_id_unknown(bad_category_name):
    # We use Nones to pad, so let them pass through
    assume(
        bad_category_name is None or bad_category_name not in aur.CATEGORIES
    )
    with assert_raises(aur.InvalidCategoryNameError):
        aur.category_name_to_id(bad_category_name)


@given(integers(min_value=2, max_value=len(aur.CATEGORIES) - 1))
def test_category_id_to_name(category_id):
    eq(
        aur.category_id_to_name(category_id),
        aur.CATEGORIES[category_id],
    )


@given(integers())
def test_category_id_to_name_unknown(bad_category_id):
    assume(bad_category_id < 2 or bad_category_id >= len(aur.CATEGORIES))
    with assert_raises(aur.InvalidCategoryIDError):
        aur.category_id_to_name(bad_category_id)
