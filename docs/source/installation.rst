Installation
============

Requirements
------------

* Python 3.7 or higher
* nanohubremote >= 1.0.0

Installing from PyPI
--------------------

The easiest way to install nanohub-results is using pip:

.. code-block:: bash

    pip install nanohub-results

Installing from Source
----------------------

You can also install from the GitHub repository:

.. code-block:: bash

    git clone https://github.com/denphi/nanohub-results.git
    cd nanohub-results
    pip install -e .

Development Installation
------------------------

For development, install with test dependencies:

.. code-block:: bash

    git clone https://github.com/denphi/nanohub-results.git
    cd nanohub-results
    pip install -e ".[dev]"

This will install additional packages needed for testing and documentation:

* pytest
* pytest-cov
* sphinx
* sphinx-rtd-theme
* myst-parser

Verifying Installation
----------------------

You can verify the installation by importing the library:

.. code-block:: python

    from nanohubresults import Results
    print("Installation successful!")

Authentication Setup
--------------------

To use the library, you'll need a nanoHUB API token:

1. Log in to nanoHUB at https://nanohub.org
2. Go to https://nanohub.org/developer
3. Generate a new personal access token
4. Use the token in your code:

.. code-block:: python

    from nanohubremote import Session
    from nanohubresults import Results

    auth_data = {
        "grant_type": "personal_token",
        "token": "YOUR_TOKEN_HERE"
    }
    session = Session(auth_data, url="https://nanohub.org/api")
    results = Results(session)
