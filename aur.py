#!/usr/bin/env python

import http.client

class QueryTooShortError(Exception):
    """Raised when the query string is too short."""
    pass

class AURClient(object):
    """Handles client requests to AUR."""
    def __init__(self):
        self.host = "aur.archlinux.org"
        self.apiPath = "/rpc.php"
        self.c = self._connect()

    def _connect(self):
        """Initialise connection to AUR."""
        return http.client.HTTPSConnection(self.host)
