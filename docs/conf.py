import sys
import os

sys.path.insert(0, os.path.abspath('..'))

project = 'aur'
version = '0.9.2'
release = version

# pylint: disable=redefined-builtin
copyright = 'Christopher Down'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]
source_suffix = '.rst'
master_doc = 'index'

exclude_patterns = ['_build']
pygments_style = 'sphinx'

html_theme = 'alabaster'
html_static_path = ['_static']

htmlhelp_basename = 'srtdoc'

autodoc_member_order = 'bysource'

intersphinx_mapping = {
    'python': ('http://docs.python.org/3.5', None),
}

autoclass_content = 'both'

# For building PDFs on ReadTheDocs
latex_documents = [
  ('index', '%s.tex' % project, '%s documentation' % project,
   copyright, 'manual'),
]


# pylint: disable=unused-argument,too-many-arguments
def no_namedtuple_attrib_docstring(app, what, name, obj, options, lines):
    if any('Alias for field number' in line for line in lines):
        # This is a namedtuple with a useless docstring, in-place purge all of
        # the lines.
        del lines[:]


def setup(app):
    app.connect('autodoc-process-docstring', no_namedtuple_attrib_docstring)
