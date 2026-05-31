# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sprawozdanie-z-laboratoriów'
copyright = '2026, Paweł Łoćwin'
author = 'Paweł Łoćwin'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for LaTeX output ------------------------------------------------
# Optymalizacja generowania PDF
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'fncychap': '\\usepackage[Bjarne]{fncychap}',
    'preamble': r'''
\setcounter{tocdepth}{2}
\raggedbottom
''',
    'sphinxsetup': 'hmargin={0.7in,0.7in}, vmargin={0.7in,0.7in}, verbatimwithframe=false',
}

latex_documents = [
    ('index', 'sprawozdanie-z-laboratoriow.tex', 'Sprawozdanie z Laboratorium: Bazy Danych', 
     'Paweł Łoćwin', 'manual'),
]

# Zmniejszenie głębi spisu treści w PDF
latex_show_urls = 'footnote'
latex_show_pagerefs = False

# Ustawienia dla obrazów w PDF
latex_max_embed_pages = 0
