'''
aur is a Python library that makes it easy to access and parse data from the
`Arch User Repository API`_.

.. _`Arch User Repository API`: https://wiki.archlinux.org/index.php/AurJson
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
    Return :py:class:`Package` objects where `package_name_substring` is a
    substring.

    >>> search('poco')
    [<Package: poco>, <Package: flopoco>, <Package: libpoco-basic>]
    '''
    return _query_api(package_name_substring, 'search')


def msearch(maintaining_user):
    '''
    Return :py:class:`Package` objects where the maintainer is
    `maintaining_user`.

    >>> msearch('cdown')
    [<Package: mpdmenu>, <Package: tzupdate>, <Package: yturl>]
    '''
    return _query_api(maintaining_user, 'msearch')


def multiinfo(package_names_or_ids):
    '''
    Return :py:class:`Package` objects matching the exact names or ids
    specified in the :term:`iterable` `package_names_or_ids`.

    Packages are returned in the form :code:`{package_name: package}` for easy
    access.

    >>> multiinfo(['yturl', 'tzupdate'])
    {'tzupdate': <Package: tzupdate>, 'yturl': <Package: yturl>}
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
            raise NoSuchPackageError(
                'Package %s missing in API response (got %r)' % (
                    reqd_pkg, got_packages,
                )
            )

    return {package.name: package for package in got_packages}


def info(package_name_or_id):
    '''
    Return the :py:class:`Package` with the exact name `package_name_or_id`.

    >>> info('linux-bfs')
    <Package: linux-bfs>
    '''
    package_multi = multiinfo([package_name_or_id])
    _, package = package_multi.popitem()
    return package


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
            raise APIError(res_data["results"])

    raw_packages = res_data['results']

    return [_raw_api_package_to_package(package) for package in raw_packages]


def _decamelcase_output(api_data):
    '''
    Decamelcase API result keys, for example OutOfDate becomes out_of_date.
    '''
    return {
        inflection.underscore(camelcased): api_value for camelcased, api_value
        in api_data.items()
    }


def _raw_api_package_to_package(raw_package_info):
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


_Package = namedtuple(
    'Package',
    [
        'num_votes', 'description', 'url_path', 'last_modified', 'name',
        'out_of_date', 'id', 'first_submitted', 'maintainer', 'version',
        'license', 'url', 'package_base', 'package_base_id', 'category_id',
    ],
)


class Package(_Package):
    '''
    All package information retrieved from the API is stored in a
    :class:`Package`, which is a :py:func:`~collections.namedtuple` with some
    extensions.

    All information about the package is available as attributes with the same
    name as those returned by the API for each package, except that each one is
    `snake case`_ instead of `Pascal case`_.

    .. _`snake case`: https://en.wikipedia.org/wiki/Snake_case
    .. _`Pascal case`: http://c2.com/cgi/wiki?PascalCase
    '''
    __slots__ = ()
    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.name)


class AURError(Exception):
    '''The base class that all AUR exceptions inherit from.'''


class APIError(AURError):
    '''
    Raised when we get a generic API error that we don't have a more specific
    exception for.
    '''

class QueryTooShortError(APIError):
    '''
    Raised when the query entered was too short. Typically, most
    :py:func:`search` queries must be at least 3 characters long.
    '''

class NoSuchPackageError(AURError):
    '''
    Raised when we explicitly requested a particular package, but we don't have
    any reference to it in the returned data, which means that the requested
    package doesn't exist.
    '''
