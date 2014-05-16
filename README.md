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

    $ pip install nose
    $ nosetests

[travis-builds]: https://travis-ci.org/cdown/gh-mirror
[travis-image]: https://travis-ci.org/cdown/gh-mirror.png?branch=master

## License

pyaur is [MIT licensed][mit]. See the LICENSE file for full details.

[mit]: http://en.wikipedia.org/wiki/MIT_license