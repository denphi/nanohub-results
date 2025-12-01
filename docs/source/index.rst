nanohub-results Documentation
==============================

**nanohub-results** is a Python library for searching and accessing simulation results from nanoHUB tools via the nanoHUB API.

This library provides a high-level query interface for filtering, sorting, and retrieving simulation data from both Rappture tools and Sim2L simulation tools on nanoHUB.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide
   api_reference
   examples
   contributing

Features
--------

* **Intuitive Query Builder**: Fluent API for building complex search queries
* **Schema Validation**: Automatic field validation against tool schemas
* **Pagination Support**: Efficient iteration over large result sets
* **Download Support**: Download output fields and simulation data
* **Type Safety**: Comprehensive type hints and runtime validation
* **Well Tested**: Full test coverage with pytest

Quick Example
-------------

.. code-block:: python

    from nanohubremote import Session
    from nanohubresults import Results

    # Initialize session
    auth_data = {
        "grant_type": "personal_token",
        "token": "YOUR_TOKEN_HERE"
    }
    session = Session(auth_data, url="https://nanohub.org/api")
    results = Results(session)

    # Search for results
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef", "output.f41") \\
        .limit(10)

    response = query.execute()
    print(f"Found {len(response['results'])} results")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
