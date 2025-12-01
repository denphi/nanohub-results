# Documentation Guide

This document describes how to build and contribute to the documentation.

## Documentation Structure

```
docs/
├── source/
│   ├── _static/          # Static files (images, CSS, etc.)
│   ├── _templates/       # Custom Sphinx templates
│   ├── conf.py          # Sphinx configuration
│   ├── index.rst        # Documentation home page
│   ├── installation.rst  # Installation instructions
│   ├── quickstart.rst   # Quick start guide
│   ├── user_guide.rst   # Detailed user guide
│   ├── api_reference.rst # API documentation
│   ├── examples.rst     # Code examples
│   └── contributing.rst # Contributing guidelines
├── requirements.txt     # Documentation dependencies
├── Makefile            # Build commands (Unix)
└── make.bat            # Build commands (Windows)
```

## Building Documentation Locally

### Prerequisites

Install documentation dependencies:

```bash
pip install -e ".[dev]"
```

Or install just the docs requirements:

```bash
pip install sphinx sphinx-rtd-theme myst-parser
```

### Build HTML Documentation

```bash
cd docs
make html
```

View the documentation:

```bash
# macOS
open build/html/index.html

# Linux
xdg-open build/html/index.html

# Windows
start build/html/index.html
```

### Build PDF Documentation

```bash
cd docs
make latexpdf
```

The PDF will be at `build/latex/nanohub-results.pdf`.

### Clean Build

Remove previous builds:

```bash
cd docs
make clean
```

## ReadTheDocs Setup

The documentation is automatically built on [ReadTheDocs](https://readthedocs.org/) when:

- Code is pushed to the main branch
- A new tag/release is created
- A pull request is opened

### Configuration

ReadTheDocs configuration is in `.readthedocs.yaml`:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.10"

sphinx:
  configuration: docs/source/conf.py

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - dev
```

### Viewing on ReadTheDocs

Once published, docs will be available at:

```
https://nanohub-results.readthedocs.io/
```

## Documentation Style Guide

### reStructuredText (RST)

Most documentation uses RST format. Here are common patterns:

**Headers**

```rst
Main Title
==========

Section
-------

Subsection
~~~~~~~~~~
```

**Code Blocks**

```rst
.. code-block:: python

    from nanohubresults import Results
    results = Results(session)
```

**Links**

```rst
:doc:`user_guide`  # Link to another doc
:ref:`section-label`  # Link to a section
`External <https://example.com>`_  # External link
```

**Lists**

```rst
* Bullet point
* Another point

1. Numbered item
2. Another item
```

**Notes and Warnings**

```rst
.. note::
    This is a note

.. warning::
    This is a warning

.. important::
    This is important
```

### Docstring Style

Use Google-style docstrings:

```python
def query(self, tool, simtool=False):
    """Create a new Query builder for a tool.

    Args:
        tool (str): Name of the tool to search.
        simtool (bool): Whether this is a simulation tool.

    Returns:
        Query: A new Query instance.

    Example:
        >>> results = Results(session)
        >>> query = results.query("2dfets", simtool=False)
    """
    pass
```

### API Documentation

API docs are auto-generated from docstrings using Sphinx autodoc:

```rst
.. autoclass:: nanohubresults.library.Results
   :members:
   :undoc-members:
   :show-inheritance:
```

## Adding New Documentation

### Add a New Page

1. Create new `.rst` file in `docs/source/`
2. Add to table of contents in `index.rst`:

```rst
.. toctree::
   :maxdepth: 2

   existing_page
   your_new_page
```

### Add Code Examples

Place examples in appropriate sections:

```rst
Basic Query
~~~~~~~~~~~

.. code-block:: python

    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef", "output.f41")

    response = query.execute()
```

### Add API Documentation

Document new classes/methods in their docstrings. Sphinx will auto-generate docs.

## Testing Documentation

### Check for Warnings

Build with warnings as errors:

```bash
make clean
sphinx-build -W -b html source build/html
```

### Spell Check

Install and run spell checker:

```bash
pip install sphinxcontrib-spelling
make spelling
```

### Link Check

Verify all links work:

```bash
make linkcheck
```

## Documentation Best Practices

1. **Write for users** - Focus on what users need to know
2. **Provide examples** - Show, don't just tell
3. **Keep it current** - Update docs with code changes
4. **Test examples** - Ensure code examples actually work
5. **Use cross-references** - Link related documentation
6. **Add screenshots** - Visual aids help understanding
7. **Include search keywords** - Help users find content

## Common Tasks

### Update API Reference

API docs auto-update from docstrings. Just update the docstrings in code.

### Add a Tutorial

1. Write tutorial in `docs/source/` as `.rst` file
2. Add to `index.rst` table of contents
3. Include working code examples
4. Build and test locally

### Fix Broken Links

```bash
make linkcheck
# Review output
# Fix broken links in source files
```

### Update Version

Update version in:

- `setup.py`
- `docs/source/conf.py`
- `pyproject.toml`

## Sphinx Extensions Used

- **sphinx.ext.autodoc** - Auto-generate API docs
- **sphinx.ext.napoleon** - Google/NumPy docstring support
- **sphinx.ext.viewcode** - Add links to source code
- **sphinx.ext.intersphinx** - Link to other projects' docs
- **myst_parser** - Markdown support

## Theme Customization

The docs use the Read the Docs theme. Customize in `conf.py`:

```python
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}
```

## Troubleshooting

### Build Fails

```bash
# Clean and rebuild
make clean
make html
```

### Missing Module Error

```bash
# Install package in development mode
pip install -e .
```

### Theme Not Found

```bash
# Install theme
pip install sphinx-rtd-theme
```

### Auto-doc Not Working

Make sure your code:
1. Has proper docstrings
2. Is importable (`pip install -e .`)
3. Is included in `api_reference.rst`

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Read the Docs Guide](https://docs.readthedocs.io/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
