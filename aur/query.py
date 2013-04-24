#!/usr/bin/env python

try: # pragma: no cover
    from http.client import HTTPSConnection
    from urllib.parse import urlencode
except ImportError:
    from httplib import HTTPSConnection
    from urllib import urlencode
import json
import sys
import aur.storageobjects
import aur.exceptions

class AURClient(object):
    """Handles client requests to AUR."""
    def __init__(self, host="aur.archlinux.org", apiPath="/rpc.php"):
        self.host = host
        self.apiPath = apiPath
        self.c = self._connect()

    def _connect(self):
        """Initialise connection to AUR."""
        return HTTPSConnection(self.host)

    def _genericSearch(self, query, queryType):
        results = self.performSingleQuery(query, queryType)
        return self.parseAURSearch(results, queryType)

    def search(self, package):
        """Perform a search on the live AUR API."""
        return self._genericSearch(package, "search")

    def msearch(self, user):
        """Perform a maintainer package search on the live AUR API."""
        return self._genericSearch(user, "msearch")

    def info(self, package):
        results = self.performSingleQuery(package, "info")
        return self.parseAURPackageInfo(results)

    def multiinfo(self, packages):
        return self._genericSearch(packages, "multiinfo")

    def performSingleQuery(self, query, queryType):
        """Perform a single query on the API."""
        self.c.request("GET", self.apiPath + "?" +
            urlencode({
                "type": queryType,
                "arg": query
            }, doseq=True)
        )
        res = self.c.getresponse()
        return json.loads(res.read().decode("utf8"))

    def parseAURSearch(self, res, queryType):
        """Parse the results of a package search."""
        if res["type"] == "error":
            if res["results"] == "Query arg too small":
                raise aur.exceptions.QueryTooShortError
            else:
                raise aur.exceptions.UnknownAURError(res["results"])
        elif res["type"] != queryType:
            raise aur.exceptions.UnexpectedResponseTypeError(res["type"])

        for result in res["results"]:
            yield aur.storageobjects.Package(**result)

    def parseAURPackageInfo(self, res):
        """Parse the results of a package search."""
        if res["type"] == "error":
            raise aur.exceptions.UnknownAURError(res["results"])
        elif res["type"] != "info":
            raise aur.exceptions.UnexpectedResponseTypeError(res["type"])

        if not res["results"]:
            raise aur.exceptions.UnknownPackageError

        return aur.storageobjects.Package(**res["results"])
