#!/usr/bin/env python

class QueryTooShortError(Exception):
    """Raised when the query string is too short."""
    pass
