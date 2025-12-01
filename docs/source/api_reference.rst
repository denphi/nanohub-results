API Reference
=============

This page contains the complete API reference for the nanohub-results library.

Results Class
-------------

.. autoclass:: nanohubresults.library.Results
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

Query Class
-----------

.. autoclass:: nanohubresults.query.Query
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

Query Methods
~~~~~~~~~~~~~

Filtering
^^^^^^^^^

.. automethod:: nanohubresults.query.Query.filter

Field Selection
^^^^^^^^^^^^^^^

.. automethod:: nanohubresults.query.Query.select

Pagination
^^^^^^^^^^

.. automethod:: nanohubresults.query.Query.limit
.. automethod:: nanohubresults.query.Query.offset

Sorting
^^^^^^^

.. automethod:: nanohubresults.query.Query.sort
.. automethod:: nanohubresults.query.Query.random

Execution
^^^^^^^^^

.. automethod:: nanohubresults.query.Query.execute
.. automethod:: nanohubresults.query.Query.paginate

Schema
^^^^^^

.. automethod:: nanohubresults.query.Query.schema

Other Methods
^^^^^^^^^^^^^

.. automethod:: nanohubresults.query.Query.revision
.. automethod:: nanohubresults.query.Query.valid_runs
.. automethod:: nanohubresults.query.Query.simtool

Results Methods
~~~~~~~~~~~~~~~

Tool Discovery
^^^^^^^^^^^^^^

.. automethod:: nanohubresults.library.Results.get_tools
.. automethod:: nanohubresults.library.Results.get_tool_detail

Querying
^^^^^^^^

.. automethod:: nanohubresults.library.Results.query
.. automethod:: nanohubresults.library.Results.search
.. automethod:: nanohubresults.library.Results.stats

Data Access
^^^^^^^^^^^

.. automethod:: nanohubresults.library.Results.get_squid_detail
.. automethod:: nanohubresults.library.Results.get_squid_files
.. automethod:: nanohubresults.library.Results.download

Database Info
^^^^^^^^^^^^^

.. automethod:: nanohubresults.library.Results.records

Constants
---------

Query.VALID_OPERATIONS
~~~~~~~~~~~~~~~~~~~~~~

Set of valid filter operations:

.. code-block:: python

    {'=', '!=', '>', '<', '>=', '<=', 'like', 'in'}

Type Hints
----------

The library uses type hints throughout for better IDE support and type checking.

Common Return Types
~~~~~~~~~~~~~~~~~~~

**Search Response**

.. code-block:: python

    {
        'success': bool,
        'results': list[dict],
        'searchTime': float,
        'code': int,
        'message': str  # Optional, on error
    }

**Tool Schema**

.. code-block:: python

    {
        'success': bool,
        'results': [{
            'tool_name': {
                'input': {
                    'field_name': {'type': str, ...},
                    ...
                },
                'output': {
                    'field_name': {'type': str, ...},
                    ...
                }
            }
        }]
    }

**Result Item**

.. code-block:: python

    {
        'squid': str,
        'input.field': value,
        'output.field': value or dict,
        ...
    }

**Curve Data**

.. code-block:: python

    {
        'xaxis': list[float],
        'yaxis': list[float]
    }

Exceptions
----------

The library raises the following exceptions:

ValueError
~~~~~~~~~~

Raised when:

* Invalid field names are used
* Invalid operations are specified
* Required methods (filter, select) are not called
* Invalid tool names are provided
* Schema validation fails

Example:

.. code-block:: python

    try:
        query.filter("invalid.field", ">", 0)
    except ValueError as e:
        print(f"Error: {e}")
        # Error: Invalid field 'invalid.field' for tool '2dfets'.
        # Available fields: ['input.Ef', 'input.Lg', ...]
