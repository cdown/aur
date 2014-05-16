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

## Testing

[![Build status][travis-image]][travis-builds]

    $ pip install -r tests/requirements.txt
    $ nosetests

[travis-builds]: https://travis-ci.org/cdown/pyaur
[travis-image]: https://travis-ci.org/cdown/pyaur.png?branch=master

## License

pyaur is [ISC licensed][isc]. See the LICENSE file for full details.

[isc]: http://en.wikipedia.org/wiki/ISC_license
