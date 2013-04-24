#!/usr/bin/env python

from nose.tools import assert_raises
import aur

a = aur.AURClient()

yturlCategoryID = a.info("yturl").categoryID

def testCategoryIDToCategoryName():
    assert aur.helpers.categoryIDToCategoryName(yturlCategoryID) == "multimedia"

def testCategoryNameToCategoryID():
    assert aur.helpers.categoryNameToCategoryID(
               aur.helpers.categoryIDToCategoryName(yturlCategoryID)
           ) == yturlCategoryID


def testBadCategoryIDToCategoryName():
    assert_raises(
        aur.exceptions.InvalidCategoryIDError,
        aur.helpers.categoryIDToCategoryName, 9999
    )

def testBadCategoryNameToCategoryID():
    assert_raises(
        aur.exceptions.InvalidCategoryNameError,
        aur.helpers.categoryNameToCategoryID, "nonexistent"
    )
