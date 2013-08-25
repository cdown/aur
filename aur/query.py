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

    def _decamelcase_output(self, api_data):
        """
        Decamelcase API output to conform to PEP8.

        :param api_data: API output data
        :returns: decamelcased API output
        """
        return {
            "num_votes":       api_data["NumVotes"],
            "description":     api_data["Description"],
            "url_path":        api_data["URLPath"],
            "last_modified":   api_data["LastModified"],
            "name":            api_data["Name"],
            "out_of_date":     api_data["OutOfDate"],
            "id":              api_data["ID"],
            "first_submitted": api_data["FirstSubmitted"],
            "maintainer":      api_data["Maintainer"],
            "version":         api_data["Version"],
            "category_id":     api_data["CategoryID"],
            "license":         api_data["License"],
            "url":             api_data["URL"],
        }

    def _generic_search(self, query, query_type, multi=False):
        """
        Perform a generic search query.

        :param query: the query to make
        :param query_type: the type of query to make
        :param multi: whether this query accepts multiple inputs
        :returns: API response for this query
        """
        res_data = self.query(query, query_type, multi)
        return self.parse_search(res_data, query_type)

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
        res_data = self.query(package, "info")
        return self.parse_info(res_data)

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

    def parse_search(self, res_data, query_type):
        """
        Parse the results of a package search.

        :param res_data: an AUR response
        :param query_type: the type of query made to get the response
        :returns: the packages for this query as Package objects
        """
        if res_data["type"] == "error":
            if res_data["results"] == "Query arg too small":
                raise aur.exceptions.QueryTooShortError
            else:
                raise aur.exceptions.UnknownAURError(res_data["results"])
        elif res_data["type"] != query_type:
            raise aur.exceptions.UnexpectedResponseTypeError(res_data["type"])

        for package in res_data["results"]:
            package = self._decamelcase_output(package)
            yield aur.Package(**package)

    def parse_info(self, res_data):
        """
        Parse the results of a package info search.

        :param res_data: an AUR response
        :returns: the package for this query as a Package object
        """
        if res_data["type"] == "error":
            raise aur.exceptions.UnknownAURError(res_data["results"])
        elif res_data["type"] != "info":
            raise aur.exceptions.UnexpectedResponseTypeError(res_data["type"])

        if not res_data["results"]:
            raise aur.exceptions.UnknownPackageError

        package = self._decamelcase_output(res_data["results"])
        return aur.Package(**package)
