#!/usr/bin/env python

from nose.tools import assert_raises
import aur

a = aur.AURClient()

yturlCategoryID = a.info("yturl").categoryID

def testCategoryIDToCategoryName():
    assert aur.helpers.category_id_to_name(yturlCategoryID) == "multimedia"

def testCategoryNameToCategoryID():
    assert aur.helpers.category_name_to_id(
               aur.helpers.category_id_to_name(yturlCategoryID)
           ) == yturlCategoryID


def testBadCategoryIDToCategoryName():
    assert_raises(
        aur.exceptions.InvalidCategoryIDError,
        aur.helpers.category_id_to_name, 9999
    )

def testBadCategoryNameToCategoryID():
    assert_raises(
        aur.exceptions.InvalidCategoryNameError,
        aur.helpers.category_name_to_id, "nonexistent"
    )
