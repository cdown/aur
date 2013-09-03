#!/usr/bin/env python

from nose.tools import assert_raises
import aur


yturl_category_id = aur.info("yturl").category_id


def test_category_id_to_name():
    assert aur.utils.category_id_to_name(yturl_category_id) == "multimedia"


def test_category_name_to_id():
    category_name = aur.utils.category_id_to_name(yturl_category_id)
    assert aur.utils.category_name_to_id(category_name) == yturl_category_id


def test_bad_category_id():
    assert_raises(
        aur.exceptions.InvalidCategoryIDError,
        aur.utils.category_id_to_name, 9999
    )


def test_bad_category_name():
    assert_raises(
        aur.exceptions.InvalidCategoryNameError,
        aur.utils.category_name_to_id, "nonexistent"
    )
