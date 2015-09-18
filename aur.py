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
CATEGORIES = (
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome",
    "i18n", "kde", "lib", "modules", "multimedia", "network", "office",
    "science", "system", "x11", "xfce", "kernels",
)
KEYS_TO_CONVERT_TO_DATETIMES = ('first_submitted', 'last_modified')

class BaseAURError(Exception): exit_code = None
class QueryTooShortError(BaseAURError): exit_code = 2
class UnknownAURError(BaseAURError): exit_code = 3
class UnknownPackageError(BaseAURError): exit_code = 5
class InvalidCategoryIDError(BaseAURError): exit_code = 6
class InvalidCategoryNameError(BaseAURError): exit_code = 7
class MissingPackageError(BaseAURError): exit_code = 8


PackageBase = namedtuple(
    'Package',
    [
        'num_votes', 'description', 'url_path', 'last_modified', 'name',
        'out_of_date', 'id', 'first_submitted', 'maintainer', 'version',
        'category_id', 'license', 'url', 'package_base', 'package_base_id',
        'popularity',
    ],
)


class Package(PackageBase):
    __slots__ = ()
    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.name)


# Extremely simple API calls that don't do anything except call query_api
def search(package): return query_api(package, 'search')
def msearch(user): return query_api(user, 'msearch')


def multiinfo(requested_packages):
    got_packages = query_api(requested_packages, 'multiinfo', multi=True)
    log.debug('Requested: %r, Got: %r', requested_packages, got_packages)

    # Check that all requests packages were retrieved. Since it's possible to
    # specify the same thing twice through a name and an id in one request, we
    # can't just check length.
    for reqd_pkg in requested_packages:
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


def info(package):
    '''
    Make an info query about a package. Internally uses multiinfo and gets the
    first result. If no results were returned, an exception is raised from
    within multiinfo.
    '''
    package_multi = list(multiinfo([package]))
    package = package_multi[0]
    return package


def category_id_to_name(category_id):
    '''
    Convert a category ID (that the API returns) into a category name (that
    would make sense to a human).
    '''
    if category_id < 0:  # Don't allow list wrap-around
        raise InvalidCategoryIDError(category_id)

    try:
        category_name = CATEGORIES[category_id]
    except IndexError:
        raise InvalidCategoryIDError(category_id)

    if category_name is None:
        raise InvalidCategoryIDError(category_id)

    return category_name



def category_name_to_id(category_name):
    '''
    Convert a category name (that would make sense to a human) into a category
    ID (that the API returns).
    '''
    # We pad the list with None, but trying to get its category makes no sense
    if category_name is None:
        raise InvalidCategoryNameError(category_name)

    try:
        return CATEGORIES.index(category_name)
    except ValueError:
        raise InvalidCategoryNameError(category_name)


def decamelcase_output(api_data):
    '''
    Decamelcase API result keys, for example OutOfDate becomes out_of_date.
    '''
    return {
        inflection.underscore(camelcased): api_value for camelcased, api_value
        in api_data.items()
    }


def query_api(query, query_type, multi=False):
    '''
    Perform a HTTP query against the AUR's API.

    If `multi` is passed, we will change the "arg" key into "arg[]", as that's
    how the AUR API expects to recieve multiple values with the same key for
    multiinfo requests.
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
    api_error_check(res_data)
    raw_packages = res_data['results']

    return [sanitise_package_info(package) for package in raw_packages]


def api_error_check(res_data):
    '''
    Perform error checking on API return data, raising distinct exception types
    for different error conditions.
    '''
    if res_data["type"] == "error":
        if res_data["results"] == "Query arg too small":
            raise QueryTooShortError
        else:
            raise UnknownAURError(res_data["results"])


def sanitise_package_info(raw_package_info):
    '''
    Sanitise package metadata, setting types appropriately, and decamelcasing
    API keys.
    '''
    pkg = decamelcase_output(raw_package_info)

    for pkg_key in pkg:
        if pkg_key not in Package._fields:
            log.warn(
                'API returned unknown package metadata, removing: %r', pkg_key,
            )
            del pkg[pkg_key]

    for date_key in KEYS_TO_CONVERT_TO_DATETIMES:
        pkg[date_key] = datetime.utcfromtimestamp(pkg[date_key])
    pkg['out_of_date'] = bool(pkg['out_of_date'])

    return Package(**pkg)
