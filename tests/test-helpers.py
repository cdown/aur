#!/usr/bin/env python

import imp
import os

aur = imp.load_source("aur", os.path.join(os.path.dirname(__file__), "../aur.py"))
helpers = imp.load_source("helpers", os.path.join(os.path.dirname(__file__), "../helpers.py"))

a = aur.AURClient()

yturlCategoryID = a.info("yturl").categoryID

def testCategoryIDToCategoryName():
    assert helpers.categoryIDToCategoryName(yturlCategoryID) == "multimedia"

def testCategoryNameToCategoryID():
    assert helpers.categoryNameToCategoryID(
               helpers.categoryIDToCategoryName(yturlCategoryID)
           ) == yturlCategoryID
