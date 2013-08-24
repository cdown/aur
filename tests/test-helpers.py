#!/usr/bin/env python

from nose.tools import assert_raises
import aur

a = aur.AURClient()

yturl_category_id = a.info("yturl").categoryID

def test_category_id_to_name():
    assert aur.helpers.category_id_to_name(yturl_category_id) == "multimedia"

def test_category_name_to_id():
    assert aur.helpers.category_name_to_id(
               aur.helpers.category_id_to_name(yturl_category_id)
           ) == yturl_category_id


def test_bad_category_id():
    assert_raises(
        aur.exceptions.InvalidCategoryIDError,
        aur.helpers.category_id_to_name, 9999
    )

def test_bad_category_name():
    assert_raises(
        aur.exceptions.InvalidCategoryNameError,
        aur.helpers.category_name_to_id, "nonexistent"
    )
