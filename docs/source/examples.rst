Examples
========

This page contains practical examples of using the nanohub-results library.

Basic Examples
--------------

Simple Search
~~~~~~~~~~~~~

.. code-block:: python

    from nanohubremote import Session
    from nanohubresults import Results

    # Initialize
    auth_data = {
        "grant_type": "personal_token",
        "token": "YOUR_TOKEN_HERE"
    }
    session = Session(auth_data, url="https://nanohub.org/api")
    results = Results(session)

    # Search for results
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef", "input.Lg", "output.f41") \\
        .limit(10)

    response = query.execute()

    # Print results
    for result in response['results']:
        print(f"SQUID: {result['squid']}")
        print(f"Ef: {result['input.Ef']}")

Multiple Filters
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Search with multiple conditions
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">=", 0.2) \\
        .filter("input.Ef", "<=", 0.4) \\
        .filter("input.Lg", ">", 15) \\
        .filter("input.temperature", "=", 300) \\
        .select("input.Ef", "input.Lg", "output.f11") \\
        .sort("input.Ef", asc=False) \\
        .limit(20)

    response = query.execute()

Advanced Examples
-----------------

Schema Exploration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def explore_tool(tool_name, simtool=False):
        """Explore available fields for a tool."""
        query = results.query(tool_name, simtool=simtool)
        fields = query.schema()

        inputs = [f for f in fields if f.startswith('input.')]
        outputs = [f for f in fields if f.startswith('output.')]

        print(f"Tool: {tool_name}")
        print(f"\\nInput fields ({len(inputs)}):")
        for field in inputs:
            print(f"  - {field}")

        print(f"\\nOutput fields ({len(outputs)}):")
        for field in outputs:
            print(f"  - {field}")

        return inputs, outputs

    # Use it
    inputs, outputs = explore_tool("2dfets", simtool=False)

Pagination with Progress
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from tqdm import tqdm

    # Query setup
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0) \\
        .select("input.Ef", "output.f41")

    # Get total count (approximate)
    first_page = results.search(
        tool="2dfets",
        filters=[{"field": "input.Ef", "operation": ">", "value": 0}],
        results_fields=["input.Ef"],
        limit=1
    )

    # Iterate with progress bar
    all_results = []
    for result in tqdm(query.paginate(per_page=100)):
        all_results.append(result)

    print(f"Collected {len(all_results)} results")

Exporting Data
~~~~~~~~~~~~~~

.. code-block:: python

    import json
    import csv
    import pandas as pd

    # Get results
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef", "input.Lg", "output.f41") \\
        .limit(100)

    response = query.execute()

    # Export to JSON
    with open('results.json', 'w') as f:
        json.dump(response['results'], f, indent=2)

    # Export metadata to CSV
    with open('metadata.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SQUID', 'Ef', 'Lg'])
        for result in response['results']:
            writer.writerow([
                result['squid'],
                result.get('input.Ef'),
                result.get('input.Lg')
            ])

    # Export to pandas DataFrame
    df = pd.DataFrame([
        {
            'squid': r['squid'],
            'Ef': r.get('input.Ef'),
            'Lg': r.get('input.Lg')
        }
        for r in response['results']
    ])
    df.to_csv('results_df.csv', index=False)

Plotting Results
~~~~~~~~~~~~~~~~

.. code-block:: python

    import matplotlib.pyplot as plt
    import numpy as np

    # Get results with curve data
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .filter("input.Ef", "<", 0.4) \\
        .select("input.Ef", "output.f41") \\
        .limit(5)

    response = query.execute()

    # Plot each curve
    fig, ax = plt.subplots(figsize=(10, 6))

    for result in response['results']:
        curve = result.get('output.f41', {})
        if curve and 'xaxis' in curve:
            ef = result.get('input.Ef')
            ax.plot(
                curve['xaxis'],
                curve['yaxis'],
                label=f"Ef={ef:.3f}V"
            )

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Output f41 for different Ef values')
    ax.legend()
    ax.grid(True)
    plt.savefig('curves.png', dpi=150)
    plt.show()

Downloading and Saving
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import json

    # Get a result
    query = results.query("st4pnjunction", simtool=True) \\
        .filter("input.temperature", ">", 0) \\
        .select("input.temperature", "output.IV Characteristic") \\
        .limit(1)

    response = query.execute()
    squid = response['results'][0]['squid']

    # Download field data
    data = results.download(
        tool="st4pnjunction",
        squid=squid,
        field="output.IV Characteristic",
        simtool=True
    )

    # Save to file
    with open('iv_data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Downloaded {len(data.get('function', []))} data points")

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

    def process_batch(tool, filters, batch_size=100):
        """Process results in batches."""
        query = results.query(tool, simtool=False) \\
            .select("input.Ef", "output.f41")

        # Add filters
        for field, op, value in filters:
            query.filter(field, op, value)

        # Process in batches
        batch = []
        batch_num = 0

        for result in query.paginate(per_page=batch_size):
            batch.append(result)

            if len(batch) >= batch_size:
                # Process batch
                print(f"Processing batch {batch_num}")
                yield batch
                batch = []
                batch_num += 1

        # Process remaining
        if batch:
            print(f"Processing final batch {batch_num}")
            yield batch

    # Use it
    filters = [
        ("input.Ef", ">", 0.2),
        ("input.Ef", "<", 0.4)
    ]

    for batch in process_batch("2dfets", filters, batch_size=50):
        # Process each batch
        print(f"Got {len(batch)} results in batch")

Simulation Tools
----------------

Working with Sim2L Tools
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Query a simulation tool
    query = results.query("st4pnjunction", simtool=True) \\
        .filter("input.temperature", "=", 300) \\
        .filter("input.p_len", ">", 0) \\
        .select(
            "input.temperature",
            "input.p_len",
            "output.IV Characteristic",
            "output.Total Current"
        ) \\
        .limit(10)

    response = query.execute()

    # Process results
    for result in response['results']:
        print(f"SQUID: {result['squid']}")
        print(f"Temperature: {result.get('input.temperature')}K")
        print(f"P-region length: {result.get('input.p_len')}nm")

AlphaFold Results
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Query AlphaFold simulations
    query = results.query("alphafold231", simtool=True) \\
        .filter("output.bestPLDDT", ">", 90) \\
        .select("output.bestPLDDT", "output.bestRanked") \\
        .sort("output.bestPLDDT", asc=False) \\
        .limit(10)

    response = query.execute()

    # Show high-confidence predictions
    for result in response['results']:
        plddt = result.get('output.bestPLDDT')
        print(f"SQUID: {result['squid']}")
        print(f"Best pLDDT: {plddt:.2f}")

Error Handling
--------------

Graceful Error Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def safe_query(tool_name, field, threshold, simtool=False):
        """Query with comprehensive error handling."""
        try:
            # Create query
            query = results.query(tool_name, simtool=simtool)

            # Validate field exists
            schema = query.schema()
            if field not in schema:
                print(f"Field '{field}' not found in tool '{tool_name}'")
                print(f"Available fields: {schema}")
                return None

            # Execute query
            query.filter(field, ">", threshold) \\
                .select(field) \\
                .limit(10)

            response = query.execute()
            return response

        except ValueError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    # Use it
    response = safe_query("2dfets", "input.Ef", 0.2, simtool=False)
    if response:
        print(f"Found {len(response['results'])} results")

Retry Logic
~~~~~~~~~~~

.. code-block:: python

    import time

    def query_with_retry(query, max_retries=3, delay=1):
        """Execute query with retry logic."""
        for attempt in range(max_retries):
            try:
                return query.execute()
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (attempt + 1))
                else:
                    raise

    # Use it
    query = results.query("2dfets", simtool=False) \\
        .filter("input.Ef", ">", 0.2) \\
        .select("input.Ef")

    response = query_with_retry(query, max_retries=3)

See Also
--------

* :doc:`user_guide` - Detailed usage information
* :doc:`api_reference` - Complete API documentation
* GitHub Examples: https://github.com/denphi/nanohub-results/tree/main/examples
