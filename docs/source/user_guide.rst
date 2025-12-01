User Guide
==========

This guide provides detailed information about using the nanohub-results library.

Understanding nanoHUB Tools
---------------------------

nanoHUB hosts two types of tools:

1. **Rappture Tools** (``simtool=False``)

   * Traditional nanoHUB tools
   * Example: ``2dfets``

2. **Simulation Tools (Sim2L)** (``simtool=True``)

   * Newer simulation framework
   * Example: ``st4pnjunction``, ``alphafold231``

Query Builder
-------------

The Query Builder provides a fluent API for constructing searches.

Creating a Query
~~~~~~~~~~~~~~~~

.. code-block:: python

    from nanohubresults import Results

    query = results.query("2dfets", simtool=False)

Required Methods
~~~~~~~~~~~~~~~~

Every query must call these methods before executing:

1. **filter()** - At least one filter condition
2. **select()** - At least one field to return

.. code-block:: python

    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef", "output.f41")

Filter Operations
~~~~~~~~~~~~~~~~~

Supported operations:

* ``=`` - Equal to
* ``!=`` - Not equal to
* ``>`` - Greater than
* ``<`` - Less than
* ``>=`` - Greater than or equal
* ``<=`` - Less than or equal
* ``like`` - Pattern matching
* ``in`` - Value in list

Examples:

.. code-block:: python

    # Numeric comparisons
    query.filter("input.Ef", ">", 0.2)
    query.filter("input.temperature", "=", 300)

    # Range queries
    query.filter("input.Ef", ">=", 0.2)
    query.filter("input.Ef", "<=", 0.4)

    # Pattern matching
    query.filter("input.material", "like", "Si%")

Field Selection
~~~~~~~~~~~~~~~

Select which fields to return in results:

.. code-block:: python

    # Select specific fields
    query.select("input.Ef", "input.Lg", "output.f41")

    # Select all inputs and outputs (not recommended for performance)
    schema = query.schema()
    query.select(*schema)

Sorting
~~~~~~~

Sort results by a field:

.. code-block:: python

    # Ascending order (default)
    query.sort("input.Ef", asc=True)

    # Descending order
    query.sort("input.Ef", asc=False)

Pagination
~~~~~~~~~~

Control which results to fetch:

.. code-block:: python

    # Limit number of results
    query.limit(50)

    # Skip first N results
    query.offset(100)

    # Combine for pagination
    query.limit(50).offset(150)  # Get results 151-200

Method Chaining
~~~~~~~~~~~~~~~

All query methods return ``self`` for easy chaining:

.. code-block:: python

    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .filter("input.Ef", "<", 0.4) \\
        .filter("input.Lg", ">", 15) \\
        .select("input.Ef", "input.Lg", "output.f41") \\
        .sort("input.Ef", asc=False) \\
        .limit(20) \\
        .offset(0)

Executing Queries
-----------------

Execute Method
~~~~~~~~~~~~~~

Execute a query and get all matching results:

.. code-block:: python

    response = query.execute()

    # Response structure
    {
        'results': [...],
        'searchTime': 0.123,
        'code': 200
    }

Paginate Method
~~~~~~~~~~~~~~~

Iterate over large result sets efficiently:

.. code-block:: python

    for result in query.paginate(per_page=100):
        # Process each result
        print(result['squid'])

The paginate method automatically:

* Fetches pages as needed
* Stops when no more results
* Handles API pagination internally

Working with Results
--------------------

Result Structure
~~~~~~~~~~~~~~~~

Each result contains:

* ``squid`` - Unique simulation identifier
* Input fields (``input.*``)
* Output fields (``output.*``)

.. code-block:: python

    result = {
        'squid': '2dfets/8/abc123...',
        'input.Ef': 0.3,
        'input.Lg': 20,
        'output.f41': {
            'xaxis': [0, 1, 2, ...],
            'yaxis': [0, 0.5, 1.0, ...]
        }
    }

Curve Data
~~~~~~~~~~

Curve outputs contain x-y data:

.. code-block:: python

    curve = result['output.f41']
    x_values = curve['xaxis']
    y_values = curve['yaxis']

    # Plot with matplotlib
    import matplotlib.pyplot as plt
    plt.plot(x_values, y_values)
    plt.show()

Scalar Values
~~~~~~~~~~~~~

Scalar outputs are simple values:

.. code-block:: python

    ef_value = result['input.Ef']
    temperature = result['input.temperature']

Schema Inspection
-----------------

Get Available Fields
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    query = results.query("2dfets", simtool=False)
    fields = query.schema()

    # Separate inputs and outputs
    inputs = [f for f in fields if f.startswith('input.')]
    outputs = [f for f in fields if f.startswith('output.')]

Tool Details
~~~~~~~~~~~~

Get comprehensive tool information:

.. code-block:: python

    tool_info = results.get_tool_detail("2dfets", simtool=False)

    # Access schema
    tool_schema = tool_info['results'][0]['2dfets']
    input_fields = tool_schema['input']
    output_fields = tool_schema['output']

List Available Tools
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # List all Rappture tools
    tools = results.get_tools(simtool=False)

    # List simulation tools
    simtools = results.get_tools(simtool=True)

Downloading Data
----------------

Download Output Fields
~~~~~~~~~~~~~~~~~~~~~~

Download specific output field data:

.. code-block:: python

    data = results.download(
        tool="st4pnjunction",
        squid="st4pnjunction/r9/abc123...",
        field="output.IV Characteristic",
        simtool=True
    )

The download method returns the raw data from the API, which may include:

* ``function`` - Array of values
* ``xaxis`` / ``yaxis`` - Curve data
* Other format-specific fields

Saving Results
--------------

Save to JSON
~~~~~~~~~~~~

.. code-block:: python

    import json

    with open('results.json', 'w') as f:
        json.dump(response['results'], f, indent=2)

Save Curves to CSV
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import csv

    curve = result['output.f41']

    with open('curve.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['X', 'Y'])
        for x, y in zip(curve['xaxis'], curve['yaxis']):
            writer.writerow([x, y])

Error Handling
--------------

Common Errors
~~~~~~~~~~~~~

**Missing Filter**

.. code-block:: python

    try:
        query.execute()
    except ValueError as e:
        # "At least one filter is required..."
        print(e)

**Missing Select**

.. code-block:: python

    try:
        query.filter("input.Ef", ">", 0).execute()
    except ValueError as e:
        # Shows all available fields
        print(e)

**Invalid Field**

.. code-block:: python

    try:
        query.filter("invalid.field", ">", 0)
    except ValueError as e:
        # "Invalid field 'invalid.field' for tool..."
        print(e)

Best Practices
--------------

1. **Always validate tools** - Check the schema before building queries
2. **Use specific selects** - Don't select all fields unless needed
3. **Paginate large results** - Use ``.paginate()`` instead of large ``.limit()``
4. **Cache schemas** - Tool schemas don't change often
5. **Handle errors gracefully** - Catch and log ``ValueError`` exceptions
6. **Set appropriate limits** - Start small when testing queries

Performance Tips
----------------

* Select only needed fields to reduce data transfer
* Use pagination for large result sets
* Filter as specifically as possible
* Sort on indexed fields when available
* Cache tool schemas to avoid repeated API calls

Advanced Usage
--------------

Random Sampling
~~~~~~~~~~~~~~~

Get random results:

.. code-block:: python

    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0) \\
        .select("input.Ef") \\
        .random(True) \\
        .limit(10)

Statistics
~~~~~~~~~~

Get statistical summaries:

.. code-block:: python

    stats = results.stats(
        tool="2dfets",
        filters=[{"field": "input.Ef", "operation": ">", "value": 0}],
        results_fields=["input.Ef"],
        limit=1000
    )

Record Counts
~~~~~~~~~~~~~

Get database statistics:

.. code-block:: python

    records = results.records(simtool=False)
    print(f"Total records: {records['total_records']}")
