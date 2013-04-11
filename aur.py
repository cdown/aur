#!/usr/bin/env python

import http.client

class QueryTooShortError(Exception):
    """Raised when the query string is too short."""
    pass

class AURClient(object):
    """Handles client requests to AUR."""
    def __init__(self, host="aur.archlinux.org", apiPath="/rpc.php"):
        self.host = host
        self.apiPath = apiPath
        self.c = self._connect()

    def _connect(self):
        """Initialise connection to AUR."""
        return http.client.HTTPSConnection(self.host)
