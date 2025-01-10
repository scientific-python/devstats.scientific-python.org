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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from datetime import date

# -- Project information -----------------------------------------------------

project = 'Scientific Python Developer Statistics'
copyright = f'2022–{date.today().year}, Scientific Python community'
author = 'Scientific Python Community'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    "analysis_template.md",
    "README.md",
    "devstats-data/*",
    "_template"
]
nb_execution_excludepatterns = ["analysis_template.md"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_favicon = '_static/favicon.ico'
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "github_url": "https://github.com/scientific-python/devstats.scientific-python.org",
    "icon_links": [
        {
            "name": "Scientific Python",
            "url": "https://scientific-python.org",
            "icon": "_static/scientific-python-logo.png",
            "type": "local",
        },
    ],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}
html_context = {"default_mode": "light"}
html_title = "Scientific Python Developer Statistics"
html_sidebars = {
    "**": []
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add build date to each page
html_last_updated_fmt = '%Y-%m-%d %H:%M%Z'
