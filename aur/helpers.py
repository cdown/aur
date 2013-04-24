#!/usr/bin/env python

import aur.exceptions

categories = [
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome", "i18n",
    "kde", "lib", "modules", "multimedia", "network", "office", "science",
    "system", "x11", "xfce", "kernels"
]

def categoryIDToCategoryName(categoryID):
    try:
        return categories[categoryID]
    except IndexError:
        raise aur.exceptions.InvalidCategoryIDError(categoryID)

def categoryNameToCategoryID(name):
    try:
        return categories.index(name)
    except ValueError:
        raise aur.exceptions.InvalidCategoryNameError(name)
