import inflection
import requests
from datetime import datetime
from collections import namedtuple

try:  # pragma: no cover
    from urllib.parse import urlencode
except ImportError:  # pragma: no cover
    from urllib import urlencode


CATEGORIES = [
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome",
    "i18n", "kde", "lib", "modules", "multimedia", "network", "office",
    "science", "system", "x11", "xfce", "kernels",
]


class QueryTooShortError(Exception): exit_code = 2
class UnknownAURError(Exception): exit_code = 3
class UnknownPackageError(Exception): exit_code = 5
class InvalidCategoryIDError(Exception): exit_code = 6
class InvalidCategoryNameError(Exception): exit_code = 7


PackageBase = namedtuple(
    'Package',
    [
        'num_votes', 'description', 'url_path', 'last_modified', 'name',
        'out_of_date', 'id', 'first_submitted', 'maintainer', 'version',
        'category_id', 'license', 'url', 'package_base', 'package_base_id',
    ],
)


class Package(PackageBase):
    __slots__ = ()
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


def category_id_to_name(category_id):
    '''
    Convert a category ID (that the API returns) into a category name (that
    would make sense to a human).
    '''
    try:
        return CATEGORIES[category_id]
    except IndexError:
        raise InvalidCategoryIDError(category_id)


def category_name_to_id(category_name):
    try:
        return CATEGORIES.index(category_name)
    except ValueError:
        raise InvalidCategoryNameError(category_name)


def search(package):
    return generic_api_query(package, "search")


def msearch(user):
    return generic_api_query(user, "msearch")


def info(package):
    package_multi = list(multiinfo([package]))
    if package_multi:
        package = package_multi[0]
        return package


def multiinfo(packages):
    return generic_api_query(packages, "multiinfo", multi=True)


def decamelcase_output(api_data):
    '''
    Decamelcase API result keys, for example OutOfDate becomes out_of_date.
    '''
    return {
        inflection.underscore(camelcased): api_value for camelcased, api_value
        in api_data.items()
    }


def generic_api_query(query, query_type, multi=False):
    '''
    Perform a generic search query.

    If `multi`, we will name all `arg` arguments as `arg[]`, in accordance with
    the API spec for multiget operations.
    '''
    res_data = query_api(query, query_type, multi)
    for package in res_data['results']:
        print(package)
        yield sanitise_package_info(package)


def query_api(query, query_type, multi=False):
    """
    Perform a single query on the AUR API.

    :param query: the search parameter(s)
    :param query_type: the type of query to make
    :param multi: whether this query accepts multiple inputs
    """
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
    api_error_check(res_data)
    return res_data


def api_error_check(res_data):
    """
    Perform error checking on API data.

    :param res_data: an AUR response
    :param query_type: the type of query made to get the response
    """
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

    for date_key in ('first_submitted', 'last_modified'):
        pkg[date_key] = datetime.utcfromtimestamp(pkg[date_key])
    pkg['out_of_date'] = bool(pkg['out_of_date'])

    return Package(**pkg)
