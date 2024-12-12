# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
from datetime import datetime

project = 'edx-name-affirmation'
copyright = f'{datetime.now().year}, edX LLC.' # pylint: disable=redefined-builtin
author = 'edX LLC'
release = '2.3.7'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"

html_theme_options = {
    "repository_url": "https://github.com/edx/edx-name-affirmation",
    "repository_branch": 'main',
    "path_to_docs": "docs/",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    # Please don't change unless you know what you're doing.
    "extra_footer": """
        <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
            <img
                alt="Creative Commons License"
                style="border-width:0"
                src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png"/>
        </a>
        <br>
        These works by
            <a
                xmlns:cc="https://creativecommons.org/ns#"
                href="https://edx.org"
                property="cc:attributionName"
                rel="cc:attributionURL"
            >edX LLC</a>
        are licensed under a
            <a
                rel="license"
                href="https://creativecommons.org/licenses/by-sa/4.0/"
            >Creative Commons Attribution-ShareAlike 4.0 International License</a>.
    """
}

html_logo = "https://logos.openedx.org/open-edx-logo-color.png"
html_favicon = "https://logos.openedx.org/open-edx-favicon.ico"

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
   os.environ['DJANGO_SETTINGS_MODULE'] = 'test_utils.test_settings'

html_static_path = ['_static']
