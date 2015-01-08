[![Build status][travis-image]][travis-builds]
[![Coverage][coveralls-image]][coveralls]
[![Code quality][scrutinizer-image]][scrutinizer]
[![Dependencies][requires-image]][requires]

[travis-builds]: https://travis-ci.org/cdown/pyaur
[travis-image]: https://img.shields.io/travis/cdown/pyaur/master.svg
[coveralls]: https://coveralls.io/r/cdown/pyaur
[coveralls-image]: https://img.shields.io/coveralls/cdown/pyaur/master.svg
[scrutinizer]: https://scrutinizer-ci.com/g/cdown/pyaur/code-structure/master/hot-spots
[scrutinizer-image]: https://img.shields.io/scrutinizer/g/cdown/pyaur.svg
[requires]: https://requires.io/github/cdown/pyaur/requirements/?branch=master
[requires-image]: https://img.shields.io/requires/github/cdown/pyaur.svg

pyaur is a Python library that makes it easy to access and parse data from the
[Arch User Repository API][api].

```python
>>> import aur
>>> list(aur.search("yturl"))
[<Package: 'yturl-git'>, <Package: 'yturl'>]
>>> package = aur.info("cower")
>>> package.description
'A simple AUR agent with a pretentious name'
```

[api]: https://wiki.archlinux.org/index.php/AurJson

## Installation

    $ pip install pyaur

## Installing dependencies

If you install by [pip][], these will be installed automatically, but
otherwise:

    $ pip install -r requirements.txt

[pip]: https://pypi.python.org/pypi/pip

## Testing

    $ pip install -r tests/requirements.txt
    $ nosetests

## License

pyaur is [ISC licensed][isc]. See the LICENSE file for full details.

[isc]: http://en.wikipedia.org/wiki/ISC_license
