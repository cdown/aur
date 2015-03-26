#!/usr/bin/env python

from collections import namedtuple

package_namedtuple = namedtuple(
    'Package',
    ['num_votes', 'description', 'url_path', 'last_modified', 'name',
     'out_of_date', 'id', 'first_submitted', 'maintainer', 'version',
     'category_id', 'license', 'url'],
)

class Package(package_namedtuple):
    r'''
    The metadata relating to a single AUR package.

    :param num_votes: The number of votes for the package (AUR API name:
                      NumVotes)
    :type num_votes: int
    :param description: The package's AUR description (AUR API name:
                        Description)
    :type description: str
    :param url_path: The path to the packaged tar.gz for this package, relative
                     to the AUR package root (AUR API name: URLPath)
    :type url_path: str
    :param last_modified: The time the package was last modified (AUR API name:
                          LastModified)
    :type last_modified: :py:class:`datetime.datetime`
    :param name: The package name (AUR API name: Name)
    :type name: str
    :param out_of_date: Whether the package is out of date or not (AUR API
                        name: OutOfDate)
    :type out_of_date: bool
    :param id: The AUR package ID (AUR API name: ID)
    :type id: int
    :param first_submitted: The time the package was first submitted (AUR API
                            name: FirstSubmitted)
    :type first_submitted: :py:class:`datetime.datetime`
    :param maintainer: The handle of the package maintainer (AUR API name:
                       Maintainer)
    :type maintainer: str
    :param version: The currently present package version (AUR API name:
                    Version)
    :type version: str
    :param category_id: The category of the package as a category ID (AUR API
                        name: CategoryID)
    :type category_id: int
    :param license: The license that the package is released under (AUR API
                    name: License)
    :type license: str
    :param url: The external URL to the project homepage, as provided by the
                package maintainer (AUR API name: URL)
    :type url: str
    '''

    __slots__ = ()

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.name)
