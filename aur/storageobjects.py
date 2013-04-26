#!/usr/bin/env python

import datetime

class Package(object):
    """Represents an AUR package and its respective metadata."""
    def __init__(self, NumVotes, Description, URLPath, LastModified, Name,
                 OutOfDate, ID, FirstSubmitted, Maintainer, Version, CategoryID,
                 License, URL):
        self.votes = NumVotes
        self.description = Description
        self.path = URLPath
        self.modified = datetime.datetime.utcfromtimestamp(LastModified)
        self.name = Name
        self.outOfDate = bool(OutOfDate)
        self.aurID = ID
        self.submitted = datetime.datetime.utcfromtimestamp(FirstSubmitted)
        self.maintainer = Maintainer
        self.version = Version
        self.categoryID = CategoryID
        self.license = License
        self.url = URL

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__dict__)
