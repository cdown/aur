#!/usr/bin/env python

import datetime


class Package(object):
    """
    Represents an AUR package and its respective metadata.
    """
    def __init__(self, num_votes, description, url_path, last_modified, name, out_of_date,
                 id, first_submitted, maintainer, version, category_id,
                 license, url):
        self.num_votes = num_votes
        self.description = description
        self.url_path = url_path
        self.last_modified = datetime.datetime.utcfromtimestamp(last_modified)
        self.name = name
        self.out_of_date = bool(out_of_date)
        self.id = id
        self.first_submitted = datetime.datetime.utcfromtimestamp(first_submitted)
        self.maintainer = maintainer
        self.version = version
        self.category_id = category_id
        self.license = license
        self.url = url

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)
