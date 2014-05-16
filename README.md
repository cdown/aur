pyaur is a Python library that makes it easy to access and parse data from the
Arch User Repository API.

Search for packages, get package info, maintainer info, and more. pyaur wraps
the official [API][] so that you can focus on using AUR data, not retrieving or
parsing it.

```python
>>> import aur
>>> list(aur.search("yturl"))
[<Package: 'yturl-git'>, <Package: 'yturl'>]
>>> package = aur.info("cower")
>>> package.description
'A simple AUR agent with a pretentious name'
>>> package.last_modified
datetime.datetime(2013, 4, 5, 0, 18, 46)
```

## Installation

    $ pip install pyaur

## Testing

[![Build status][travis-image]][travis-builds]

To run the tests yourself:

    $ pip install nose
    $ nosetests
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 6.720s

    OK

## License

pyaur is MIT licensed. See the LICENSE file for full details.

[travis-builds]: https://travis-ci.org/cdown/gh-mirror
[travis-image]: https://travis-ci.org/cdown/gh-mirror.png?branch=master
[API]: https://wiki.archlinux.org/index.php/AurJson
