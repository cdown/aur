#!/usr/bin/env python


class QueryTooShortError(Exception):
    """
    Raised when the query string is too short.
    """
    pass


class UnknownAURError(Exception):
    """
    Raised when we receive an unknown AUR error.
    """
    pass


class UnexpectedResponseTypeError(Exception):
    """
    Raised when we receive an response type that is inappropriate for our
    request.
    """
    pass


class UnknownPackageError(Exception):
    """
    Raised when we make an info query, but the package does not exist.
    """
    pass


class InvalidCategoryIDError(Exception):
    """
    Raised when an invalid category ID is given.
    """
    pass


class InvalidCategoryNameError(Exception):
    """
    Raised when an invalid category name is given.
    """
    pass
