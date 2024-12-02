import os
import sys
import shutil
# Répertoire racine de ton projet
sys.path.insert(0, os.path.abspath('../src/optimRecipes'))


def copy_custom_index(app, exception):
    if exception is None:  # Ensure the build was successful
        source = os.path.abspath("docs/index.html")  # Path to your custom index.html
        # Target path in build directory
        destination = os.path.join(app.outdir, "index.html")
        if os.path.exists(source):
            shutil.copyfile(source, destination)


def setup(app):
    app.connect("build-finished", copy_custom_index)
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'KIT-BIG-DATA'
copyright = '2024, Groupe projet big data'
author = 'Groupe projet big data'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Supporte le style NumPy et Google des docstrings
]

# Configuration pour autodoc
autodoc_default_options = {
    'members': True,  # Inclure les membres publics
    'private-members': True,  # Inclure les membres privés (_nom)
}

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_baseurl = 'https://zeinagebran.github.io/KIT-BIG-DATA/'
html_context = {
    "display_github": True,
    "github_user": "zeinagebran",
    "github_repo": "KIT-BIG-DATA",
    "github_version": "master",  # or the branch you are deploying from
    "conf_py_path": "/docs/",
}
