#!/usr/bin/env python

import aur
import aur.exceptions
import json
import sys

try:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode
except ImportError:
    from httplib import HTTPSConnection
    from urllib import urlencode


class AURClient(object):
    """
    Handles client requests to AUR.
    """
    def __init__(self, api_host="aur.archlinux.org", api_path="/rpc.php?"):
        self.api_host = api_host
        self.api_path = api_path
        self.c = self._connect()

    def _connect(self):
        """
        Initialise connection to AUR.

        :returns: a HTTPSConnection to the AUR
        """
        return HTTPSConnection(self.api_host)

    def _decamelcase_output(self, pkg_info):
        """
        Decamelcase API output to conform to PEP8.

        :param pkg_info: API output data
        :returns: decamelcased API output
        """
        return {
            "num_votes":       pkg_info["NumVotes"],
            "description":     pkg_info["Description"],
            "url_path":        pkg_info["URLPath"],
            "last_modified":   pkg_info["LastModified"],
            "name":            pkg_info["Name"],
            "out_of_date":     pkg_info["OutOfDate"],
            "id":              pkg_info["ID"],
            "first_submitted": pkg_info["FirstSubmitted"],
            "maintainer":      pkg_info["Maintainer"],
            "version":         pkg_info["Version"],
            "category_id":     pkg_info["CategoryID"],
            "license":         pkg_info["License"],
            "url":             pkg_info["URL"],
        }

    def _generic_search(self, query, query_type, multi=False):
        """
        Perform a generic search query.

        :param query: the query to make
        :param query_type: the type of query to make
        :param multi: whether this query accepts multiple inputs
        :returns: API response for this query
        """
        results = self.query(query, query_type, multi)
        return self.parse_search(results, query_type)

    def search(self, package):
        """
        Perform a search on the AUR API.

        :param package: the package name to search for
        :returns: API response for this query
        """
        return self._generic_search(package, "search")

    def msearch(self, user):
        """
        Perform a maintainer package search on the AUR API.

        :param user: the user to search for
        :returns: API response for this query
        """
        return self._generic_search(user, "msearch")

    def info(self, package):
        """
        Perform an info search on the AUR API.

        :param package: the package to get information about
        :returns: API response for this query
        """
        results = self.query(package, "info")
        return self.parse_info(results)

    def multiinfo(self, packages):
        """
        Perform a multiinfo search on the AUR API.

        :param packages: the packages to get information about
        :returns: API response for this query
        """
        return self._generic_search(packages, "multiinfo", multi=True)

    def query(self, query, query_type, multi=False):
        """
        Perform a single query on the AUR API.

        :param query: the search parameter(s)
        :param query_type: the type of query to make
        :param multi: whether this query accepts multiple inputs
        """
        query_key = "arg"
        if multi:
            query_key += "[]"

        self.c.request(
            "GET",
            self.api_path + urlencode({
                "type": query_type,
                query_key: query
            }, doseq=True)
        )
        res_handle = self.c.getresponse()

        # Annoyingly, the AUR API does not send any indication of the content's
        # character encoding. web/lib/aurjson.class.php shows that the AUR
        # returns data from json_encode(), which means that we should always
        # get UTF8 (but still, meh).
        res_data_raw = res_handle.read()
        res_encoding = "utf8"
        res_data = json.loads(res_data_raw.decode(res_encoding))

        return res_data

    def parse_search(self, res, query_type):
        """
        Parse the results of a package search.

        :param res: an AUR response
        :param query_type: the type of query made to get the response
        :returns: the packages for this query as Package objects
        """
        if res["type"] == "error":
            if res["results"] == "Query arg too small":
                raise aur.exceptions.QueryTooShortError
            else:
                raise aur.exceptions.UnknownAURError(res["results"])
        elif res["type"] != query_type:
            raise aur.exceptions.UnexpectedResponseTypeError(res["type"])

        for result in res["results"]:
            result = self._decamelcase_output(result)
            yield aur.Package(**result)

    def parse_info(self, res):
        """
        Parse the results of a package info search.

        :param res: an AUR response
        :returns: the package for this query as a Package object
        """
        if res["type"] == "error":
            raise aur.exceptions.UnknownAURError(res["results"])
        elif res["type"] != "info":
            raise aur.exceptions.UnexpectedResponseTypeError(res["type"])

        if not res["results"]:
            raise aur.exceptions.UnknownPackageError

        res = self._decamelcase_output(res["results"])
        return aur.Package(**res)
