Quick Start Guide
=================

This guide will help you get started with the nanohub-results library.

Basic Setup
-----------

First, import the necessary modules and create a session:

.. code-block:: python

    from nanohubremote import Session
    from nanohubresults import Results

    # Initialize session with your API token
    auth_data = {
        "grant_type": "personal_token",
        "token": "YOUR_TOKEN_HERE"
    }
    session = Session(auth_data, url="https://nanohub.org/api")
    results = Results(session)

Exploring Tool Schemas
----------------------

Before querying, you can explore what fields are available for a tool:

.. code-block:: python

    # Create a query to get the schema
    query = results.query("2dfets", simtool=False)
    schema = query.schema()

    # Print available fields
    for field in schema:
        print(field)

Basic Query
-----------

Here's a simple query to search for results:

.. code-block:: python

    # Build and execute a query
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef", "input.Lg", "output.f41") \\
        .limit(10)

    response = query.execute()

    # Process results
    for result in response['results']:
        print(f"SQUID: {result['squid']}")
        print(f"Fermi Energy: {result['input.Ef']}")
        print(f"Gate Length: {result['input.Lg']}")

Key Requirements
----------------

.. important::

    The API requires you to:

    1. Add at least one ``.filter()`` condition
    2. Add at least one ``.select()`` field

    Without these, you'll get a helpful error message showing available fields.

Multiple Filters
----------------

You can chain multiple filters together:

.. code-block:: python

    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .filter("input.Ef", "<", 0.4) \\
        .filter("input.Lg", ">", 15) \\
        .select("input.Ef", "input.Lg", "output.f41") \\
        .sort("input.Ef", asc=False) \\
        .limit(20)

    response = query.execute()

Working with Simulation Tools
------------------------------

For simulation tools (Sim2L), set ``simtool=True``:

.. code-block:: python

    query = results.query("st4pnjunction", simtool=True) \\
        .filter("input.temperature", ">", 0) \\
        .select("input.temperature", "output.IV Characteristic") \\
        .limit(5)

    response = query.execute()

Pagination
----------

For large result sets, use pagination:

.. code-block:: python

    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0) \\
        .select("input.Ef", "output.f41")

    # Iterate over all results
    for result in query.paginate(per_page=50):
        print(f"Processing: {result['squid']}")

Downloading Data
----------------

Download specific output fields:

.. code-block:: python

    # Get a result first
    query = results.query("st4pnjunction", simtool=True) \\
        .filter("input.temperature", ">", 0) \\
        .select("input.temperature", "output.IV Characteristic") \\
        .limit(1)

    response = query.execute()
    squid = response['results'][0]['squid']

    # Download specific field data
    data = results.download(
        tool="st4pnjunction",
        squid=squid,
        field="output.IV Characteristic",
        simtool=True
    )

    print(f"Downloaded {len(data.get('function', []))} data points")

Error Handling
--------------

The library provides helpful error messages:

.. code-block:: python

    try:
        # This will fail - no .select()
        query = results.query("2dfets", simtool=False) \\
            .filter("input.Ef", ">", 0)
        query.execute()
    except ValueError as e:
        print(e)  # Shows all available fields

Next Steps
----------

* Read the :doc:`user_guide` for detailed information
* Check the :doc:`api_reference` for complete API documentation
* Explore the :doc:`examples` for more use cases
