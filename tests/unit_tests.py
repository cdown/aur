#!/usr/bin/env python

import json
import types
import os
import mock
import aur
import httpretty
import re
from nose_parameterized import parameterized
from nose.tools import eq_ as eq, assert_raises
from hypothesis import given, assume
import testfixtures
import hypothesis.strategies as st


SAMPLE_DIR = os.path.join(os.path.dirname(__file__), 'samples')

@parameterized([
    'msearch_found',
    'msearch_not_found',
    'multiinfo_found',
    ('multiinfo_not_found', aur.NoSuchPackageError),
    ('multiinfo_only_partial_found', aur.NoSuchPackageError),
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
    elif isinstance(got, dict):
        got = {pkg_name: vars(pkg) for pkg_name, pkg in got.items()}
    else:
        got = vars(got)

    # Since we can't store all data types in the JSON, we store them the same
    # way the API would return them. Convert them back here.
    for conversion_func, pkg_keys in aur._TYPE_CONVERSION_FUNCTIONS.items():
        if isinstance(expected, list):
            for package in expected:
                for pkg_key in pkg_keys:
                    package[pkg_key] = conversion_func(package[pkg_key])
        elif isinstance(expected, dict):
            for _, package in expected.items():
                for pkg_key in pkg_keys:
                    package[pkg_key] = conversion_func(package[pkg_key])
        else:
            for pkg_key in pkg_keys:
                expected[pkg_key] = conversion_func(expected[pkg_key])

    eq(got, expected)


@given(st.text())
def test_info(package):
    # This test relies on the fact that info() doesn't actually care whether it
    # has a real Package object or not. If that changes, it needs to be
    # reevaluated.
    #
    # info() just uses .popitem(), so the package name key doesn't matter.
    with mock.patch('aur.multiinfo', return_value={'_': package}) as mi_mock:
        got = aur.info(package)
    mi_mock.assert_called_once_with([package])
    eq(got, package)


@given(st.lists(st.text(), min_size=1))
def test_unknown_package_keys_are_removed_and_warn(unknown_package_keys):
    known_package_keys = list(aur.Package._fields)
    assume(not any(upk in known_package_keys for upk in unknown_package_keys))

    with open(os.path.join(SAMPLE_DIR, 'search_found.api_response')) as api_f:
        api_output = json.load(api_f)

    raw_package = api_output['results'][0]

    # Add bogus keys to trigger warning
    for key in unknown_package_keys:
        raw_package[key] = None

    # If the keys were not successfully deleted, this will raise a TypeError
    with testfixtures.LogCapture() as logs:
        aur._raw_api_package_to_package(raw_package)

    print(logs)
    logs.check(
        (
            'aur', 'WARNING',
            testfixtures.StringComparison(
                'API returned unknown package metadata, removing:'
            ),
        )
    )
