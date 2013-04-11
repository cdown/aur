#!/usr/bin/env python

import http.client
import json
import urllib.parse
import datetime

class QueryTooShortError(Exception):
    """Raised when the query string is too short."""
    pass

class UnknownAURError(Exception):
    """Raised when we receive an unknown AUR error."""
    pass

class UnexpectedResponseTypeError(Exception):
    """Raised when we receive an response type that is inappropriate for our
       request."""
    pass

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

class AURClient(object):
    """Handles client requests to AUR."""
    def __init__(self, host="aur.archlinux.org", apiPath="/rpc.php"):
        self.host = host
        self.apiPath = apiPath
        self.c = self._connect()

    def _connect(self):
        """Initialise connection to AUR."""
        return http.client.HTTPSConnection(self.host)

    def _getEncoding(self, headers, fallback="utf8"):
        """Finds the encoding for a response, or falls back to a default."""
        preferences = (
            headers.get_content_charset(),
            headers.get_charset(),
            fallback
        )

        for preference in preferences:
            if preference != None:
                return preference

    def search(self, package):
        """Perform a search on the live AUR API."""
        results = self.performSearch(package)
        parsed = self.parseSearch(results)
        return parsed

    def performSearch(self, package):
        """Perform a package search."""
        self.c.request("GET", self.apiPath + "?" +
            urllib.parse.urlencode({
                "type": "search",
                "arg": package
            })
        )
        res = self.c.getresponse()
        encoding = self._getEncoding(res.headers)
        return json.loads(res.read().decode(encoding))

    def parseSearch(self, res):
        """Parse the results of a package search."""
        if res["type"] == "error":
            if res["results"] == "Query arg too small":
                raise QueryTooShortError
            else:
                raise UnknownAURError(res["results"])
        elif res["type"] != "search":
            raise UnexpectedResponseTypeError(res["type"])

        for result in res["results"]:
            yield Package(**result)
