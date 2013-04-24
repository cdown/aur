#!/usr/bin/env python

import aur

a = aur.AURClient()

yturlCategoryID = a.info("yturl").categoryID

def testCategoryIDToCategoryName():
    assert aur.helpers.categoryIDToCategoryName(yturlCategoryID) == "multimedia"

def testCategoryNameToCategoryID():
    assert aur.helpers.categoryNameToCategoryID(
               aur.helpers.categoryIDToCategoryName(yturlCategoryID)
           ) == yturlCategoryID
