#!/usr/bin/env python

import aur
import aur.exceptions
import json
import requests
import sys

try: # pragma: no cover
    from urllib.parse import urlencode
except ImportError: # pragma: no cover
    from urllib import urlencode


class AURClient(object):
    """
    Handles client requests to AUR.
    """
    def __init__(self, api_url="http://aur.archlinux.org/rpc.php?"):
        self.api_url = api_url

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
        return self.parse_multi(res_data, query_type)

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
        return self.parse_single(res_data, "info")

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

        res_handle = requests.get(
            self.api_url + urlencode({
                "type": query_type,
                query_key: query
            }, doseq=True)
        )
        res_data = res_handle.json()

        return res_data

    def _api_error_check(self, res_data, query_type):
        """
        Perform error checking on API data.

        :param res_data: an AUR response
        :param query_type: the type of query made to get the response
        """
        if res_data["type"] == "error":
            if res_data["results"] == "Query arg too small":
                raise aur.exceptions.QueryTooShortError
            else:
                raise aur.exceptions.UnknownAURError(res_data["results"])
        elif res_data["type"] != query_type:
            raise aur.exceptions.UnexpectedResponseTypeError(res_data["type"])

    def parse_multi(self, res_data, query_type):
        """
        Parse the results of a package search.

        :param res_data: an AUR response
        :param query_type: the type of query made to get the response
        :returns: the packages for this query as Package objects
        """
        self._api_error_check(res_data, query_type)

        for package in res_data["results"]:
            package = self._decamelcase_output(package)
            yield aur.Package(**package)

    def parse_single(self, res_data, query_type):
        """
        Parse the results of a package info search.

        :param res_data: an AUR response
        :returns: the package for this query as a Package object
        """
        self._api_error_check(res_data, query_type)

        package = self._decamelcase_output(res_data["results"])
        return aur.Package(**package)
