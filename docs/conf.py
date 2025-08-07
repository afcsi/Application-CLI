import os
import sys
from datetime import date

# Permet à autodoc d'importer src/task_manager
sys.path.insert(0, os.path.abspath('../src'))

project = 'Application-CLI'
author = 'afcsi'
copyright = f'{date.today().year}, {author}'

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',        # Google/NumPy docstrings
    'sphinx.ext.viewcode',
]

myst_enable_extensions = ["colon_fence"]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
