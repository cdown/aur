#!/usr/bin/env python

from datetime import datetime


class Package(object):
    """
    Represents an AUR package and its respective metadata.
    """
    def __init__(self, num_votes, description, url_path, last_modified, name,
                 out_of_date, id, first_submitted, maintainer, version,
                 category_id, license, url):
        for k, v in locals().items():
            if k != "self":
                setattr(self, k, v)

        self.first_submitted = datetime.utcfromtimestamp(first_submitted)
        self.last_modified = datetime.utcfromtimestamp(last_modified)
        self.out_of_date = bool(out_of_date)

    def __repr__(self):  # pragma: no cover
        return "<%s: %r>" % (self.__class__.__name__, self.name)
