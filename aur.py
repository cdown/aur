'''
aur is a Python library that makes it easy to access and parse data from the
[Arch User Repository API](https://wiki.archlinux.org/index.php/AurJson).
'''

import inflection
import requests
from datetime import datetime
from collections import namedtuple
import logging

try:
    from urllib.parse import urlencode
except ImportError:  # Python 2 fallback
    from urllib import urlencode


log = logging.getLogger(__name__)

# A map of category id (list index) to category name mappings. See
# category_id_to_name and category_name_to_id. "None" entries are just padding
# since category ids start at 2, which is in this case represented by index 2.
_CATEGORIES = (
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome",
    "i18n", "kde", "lib", "modules", "multimedia", "network", "office",
    "science", "system", "x11", "xfce", "kernels",
)

# Type conversions to perform after getting API return data. For example,
# first_submitted and last_modified are returned as epochs in the API response,
# and they get converted into datetime objects before being passed to the
# Package object.
_TYPE_CONVERSION_FUNCTIONS = {
    datetime.utcfromtimestamp: ['first_submitted', 'last_modified'],
    bool: ['out_of_date'],
}


def search(package_name_substring):
    '''
    Return `aur.Package`s where `package_name_substring` is a substring.
    '''
    return _query_api(package_name_substring, 'search')


def msearch(maintaining_user):
    '''
    Return `aur.Package`s where the maintainer is `maintaining_user`.
    '''
    return _query_api(maintaining_user, 'msearch')


def multiinfo(package_names_or_ids):
    '''
    Return `aur.Package`s matching the exact names or ids specified in
    `package_names_or_ids`.
    '''
    got_packages = _query_api(package_names_or_ids, 'multiinfo', multi=True)
    log.debug('Requested: %r, Got: %r', package_names_or_ids, got_packages)

    # Check that all requests packages were retrieved. Since it's possible to
    # specify the same thing twice through a name and an id in one request, we
    # can't just check length.
    for reqd_pkg in package_names_or_ids:
        for got_pkg in got_packages:
            if reqd_pkg == got_pkg.name or reqd_pkg == got_pkg.id:
                log.debug('Requested package %s matched %s', reqd_pkg, got_pkg)
                break
        else:
            raise MissingPackageError(
                'Package %s missing in API response (got %r)' % (
                    reqd_pkg, got_packages,
                )
            )

    return got_packages


def info(package_name_or_id):
    '''Return the `aur.Package` with the exact name `package_name_or_id`.'''
    package_multi = multiinfo([package_name_or_id])
    package = package_multi[0]
    return package


def category_id_to_name(category_id):
    '''
    Convert a category ID (that the API returns) into a category name (that
    would make sense to a human).

    For example, category ID 2 maps to category name "daemons".
    '''
    if category_id < 0:  # Don't allow list wrap-around
        raise InvalidCategoryIDError(category_id)

    try:
        category_name = _CATEGORIES[category_id]
    except IndexError:
        raise InvalidCategoryIDError(category_id)

    if category_name is None:
        raise InvalidCategoryIDError(category_id)

    return category_name



def category_name_to_id(category_name):
    '''
    Convert a category name (that would make sense to a human) into a category
    ID (that the API returns).

    For example, category name "daemons" maps to category ID 2.
    '''
    # We pad the list with None, but trying to get its category makes no sense
    if category_name is None:
        raise InvalidCategoryNameError(category_name)

    try:
        return _CATEGORIES.index(category_name)
    except ValueError:
        raise InvalidCategoryNameError(category_name)


def _query_api(query, query_type, multi=False):
    '''
    Perform a HTTP query against the AUR's API.

    If `multi` is passed, we will change the "arg" key passed to the AUR API
    into "arg[]", as that's how the AUR API expects to recieve multiple values
    with the same key for multiinfo requests.
    '''
    log.debug('Making API query with query_type %s', query_type)
    query_key = "arg"
    if multi:
        query_key += "[]"

    res_handle = requests.get(
        "https://aur.archlinux.org/rpc.php?" + urlencode({
            "type": query_type,
            query_key: query
        }, doseq=True)
    )

    res_data = res_handle.json()
    log.debug('API returned: %r', res_data)

    if res_data["type"] == "error":
        if res_data["results"] == "Query arg too small":
            raise QueryTooShortError(res_data['results'])
        else:
            raise UnknownAURError(res_data["results"])

    raw_packages = res_data['results']

    return [_sanitise_package_info(package) for package in raw_packages]


def _decamelcase_output(api_data):
    '''
    Decamelcase API result keys, for example OutOfDate becomes out_of_date.
    '''
    return {
        inflection.underscore(camelcased): api_value for camelcased, api_value
        in api_data.items()
    }


def _sanitise_package_info(raw_package_info):
    '''
    Sanitise package metadata, setting types appropriately, and decamelcasing
    API keys.
    '''
    pkg = _decamelcase_output(raw_package_info)

    keys_to_rm = set(pkg) - set(Package._fields)
    if keys_to_rm:
        log.warning(
            'API returned unknown package metadata, removing: %r', keys_to_rm,
        )

    for key in keys_to_rm:
        del pkg[key]

    for conversion_func, pkg_keys in _TYPE_CONVERSION_FUNCTIONS.items():
        for pkg_key in pkg_keys:
            pkg[pkg_key] = conversion_func(pkg[pkg_key])

    return Package(**pkg)


class BaseAURError(Exception): exit_code = None
class QueryTooShortError(BaseAURError): exit_code = 2
class UnknownAURError(BaseAURError): exit_code = 3
class UnknownPackageError(BaseAURError): exit_code = 5
class InvalidCategoryIDError(BaseAURError): exit_code = 6
class InvalidCategoryNameError(BaseAURError): exit_code = 7
class MissingPackageError(BaseAURError): exit_code = 8


_Package = namedtuple(
    'Package',
    [
        'num_votes', 'description', 'url_path', 'last_modified', 'name',
        'out_of_date', 'id', 'first_submitted', 'maintainer', 'version',
        'category_id', 'license', 'url', 'package_base', 'package_base_id',
        'popularity',
    ],
)


class Package(_Package):
    __slots__ = ()
    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.name)
