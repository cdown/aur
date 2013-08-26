#!/usr/bin/env python

import aur.exceptions


categories = [
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome",
    "i18n", "kde", "lib", "modules", "multimedia", "network", "office",
    "science", "system", "x11", "xfce", "kernels",
]


def category_id_to_name(category_id):
    """
    Convert a category ID to a category name.

    :param category_id: the category ID to convert
    :returns: the associated category name
    """

    try:
        return categories[category_id]
    except IndexError:
        raise aur.exceptions.InvalidCategoryIDError(category_id)


def category_name_to_id(category_name):
    """
    Convert a category name to a category ID.

    :param category_name: the category name to convert
    :returns: the associated category ID
    """

    try:
        return categories.index(category_name)
    except ValueError:
        raise aur.exceptions.InvalidCategoryNameError(category_name)
