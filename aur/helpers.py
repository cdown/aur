#!/usr/bin/env python

import aur.exceptions


categories = [
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome",
    "i18n", "kde", "lib", "modules", "multimedia", "network", "office",
    "science", "system", "x11", "xfce", "kernels",
]


def category_id_to_name(cat_id):
    try:
        return categories[cat_id]
    except IndexError:
        raise aur.exceptions.InvalidCategoryIDError(cat_id)


def category_name_to_id(cat_name):
    try:
        return categories.index(cat_name)
    except ValueError:
        raise aur.exceptions.InvalidCategoryNameError(cat_name)
