Contributing
============

Thank you for considering contributing to nanohub-results! This document provides guidelines for contributing to the project.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

    git clone https://github.com/YOUR_USERNAME/nanohub-results.git
    cd nanohub-results

3. Install development dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

4. Create a branch for your changes:

.. code-block:: bash

    git checkout -b feature/your-feature-name

Development Workflow
--------------------

Running Tests
~~~~~~~~~~~~~

Run the full test suite:

.. code-block:: bash

    pytest

Run with coverage:

.. code-block:: bash

    pytest --cov=nanohubresults --cov-report=html

Run specific tests:

.. code-block:: bash

    pytest tests/test_query.py::TestQueryFiltering::test_filter_valid_field

Code Style
~~~~~~~~~~

The project follows PEP 8 style guidelines. Format your code before committing:

.. code-block:: bash

    # Install formatters (if not already installed)
    pip install black isort

    # Format code
    black nanohubresults tests
    isort nanohubresults tests

Type Checking
~~~~~~~~~~~~~

The project uses type hints. Check types with mypy:

.. code-block:: bash

    pip install mypy
    mypy nanohubresults

Documentation
~~~~~~~~~~~~~

Build documentation locally:

.. code-block:: bash

    cd docs
    make html

View the built docs at ``docs/build/html/index.html``.

Contribution Guidelines
-----------------------

Code Contributions
~~~~~~~~~~~~~~~~~~

1. **Write tests** - All new features should include tests
2. **Update documentation** - Update relevant docs for your changes
3. **Follow style** - Use black and isort for formatting
4. **Add type hints** - Include type hints for new functions
5. **Write docstrings** - Use Google-style docstrings

Example docstring:

.. code-block:: python

    def my_function(param1: str, param2: int) -> dict:
        """Brief description of function.

        Longer description providing more details about
        what the function does and how to use it.

        Args:
            param1: Description of param1
            param2: Description of param2

        Returns:
            Description of return value

        Raises:
            ValueError: When param1 is invalid

        Example:
            >>> my_function("test", 42)
            {'result': 'success'}
        """
        pass

Pull Request Process
~~~~~~~~~~~~~~~~~~~~

1. Update the README.md if needed
2. Update the documentation if needed
3. Add tests for new functionality
4. Ensure all tests pass
5. Update the CHANGELOG (if exists)
6. Submit a pull request with a clear description

PR Description Template:

.. code-block:: text

    ## Description
    Brief description of the changes

    ## Type of Change
    - [ ] Bug fix
    - [ ] New feature
    - [ ] Documentation update
    - [ ] Code refactoring

    ## Testing
    Describe the tests you ran

    ## Checklist
    - [ ] Tests pass locally
    - [ ] Added/updated tests
    - [ ] Updated documentation
    - [ ] Code follows style guidelines
    - [ ] Added type hints

Reporting Issues
----------------

Bug Reports
~~~~~~~~~~~

When reporting bugs, please include:

1. Python version
2. nanohub-results version
3. Operating system
4. Steps to reproduce
5. Expected behavior
6. Actual behavior
7. Error messages/tracebacks

Feature Requests
~~~~~~~~~~~~~~~~

When requesting features, please:

1. Explain the use case
2. Describe the desired behavior
3. Provide examples if possible
4. Explain why this would be useful

Security Issues
~~~~~~~~~~~~~~~

Do not report security issues in public issues. Email the maintainers directly.

Code of Conduct
---------------

Be Respectful
~~~~~~~~~~~~~

* Be welcoming and inclusive
* Respect differing viewpoints
* Accept constructive criticism gracefully
* Focus on what's best for the community

Unacceptable Behavior
~~~~~~~~~~~~~~~~~~~~~

* Harassment or discriminatory language
* Personal attacks
* Trolling or insulting comments
* Publishing others' private information

Development Guidelines
----------------------

Adding New Features
~~~~~~~~~~~~~~~~~~~

1. Discuss the feature in an issue first
2. Keep changes focused and atomic
3. Write comprehensive tests
4. Update documentation
5. Follow existing patterns in the codebase

Testing Guidelines
~~~~~~~~~~~~~~~~~~

* Write unit tests for all new code
* Aim for >90% code coverage
* Test edge cases and error conditions
* Use descriptive test names
* Mock external dependencies

Documentation Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

* Update docstrings for all public APIs
* Add examples for new features
* Update user guide if needed
* Keep README.md up to date
* Build docs locally to verify

Release Process
---------------

(For Maintainers)

1. Update version in ``setup.py`` and ``pyproject.toml``
2. Update CHANGELOG.md
3. Run full test suite
4. Build and test package locally
5. Create git tag
6. Push to PyPI
7. Create GitHub release

Questions?
----------

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label
4. Join discussions on GitHub

Thank You!
----------

Your contributions make this project better. Thank you for taking the time to contribute!
