# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# noinspection PyProtectedMember
from sphinx.ext.autodoc import ClassDocumenter, _

sys.path.insert(0, os.path.abspath('..'))

add_line = ClassDocumenter.add_line
line_to_delete = _(u'Bases: %s') % u':class:`object`'


# Tohle je prostě rychle udělaný patch zkopírovaný odsud:
# https://stackoverflow.com/questions/46279030/how-can-i-prevent-sphinx-from-listing-object-as-a-base-class
def add_line_no_object_base(self, text, *args, **kwargs):
    if text.strip() == line_to_delete:
        return
    add_line(self, text, *args, **kwargs)


add_directive_header = ClassDocumenter.add_directive_header


def add_directive_header_no_object_base(self, *args, **kwargs):
    # noinspection PyArgumentList
    self.add_line = add_line_no_object_base.__get__(self)
    # noinspection PyNoneFunctionAssignment
    result = add_directive_header(self, *args, **kwargs)
    del self.add_line
    return result


ClassDocumenter.add_directive_header = add_directive_header_no_object_base


def data_import(inp="../data_import.py"):
    with open(inp, "r") as file:
        lines = file.readlines()
    lines = lines[1:]
    for i, text in enumerate(lines):
        lines[i] = ">>> " + text
    lines = "".join(lines)
    output = "```pycon\n" + lines + "```\n"
    return output


# -- Project information -----------------------------------------------------

project = 'Prohlížeč dat počasí'
# noinspection PyShadowingBuiltins
copyright = '2022, Roman Táborský'
author = 'Roman Táborský'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",  # Je použité v některých docstrings
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.viewcode"
]

myst_enable_extensions = [
    "colon_fence",
    "replacements",
    "substitution"
]

myst_substitutions = {
    "data_import": data_import()
}

autosectionlabel_prefix_document = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Intersphinx mappings
intersphinx_mapping = {'pandas': ('https://pandas.pydata.org/pandas-docs/stable', None)}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'cs'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_title = project
html_favicon = 'favicon.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
