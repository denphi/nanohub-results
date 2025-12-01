import sys
import os
import json

# Add parent directory to path for local development
sys.path.insert(0, os.path.abspath('..'))

from nanohubremote import Session
from nanohubresults import Results

def print_schema(tool_name, simtool=True):
    """
    Helper function to print tool schema in a readable format.

    Args:
        tool_name: Name of the tool to inspect
        simtool: Whether this is a simulation tool
    """
    print(f"\n{'='*60}")
    print(f"Schema for tool: {tool_name} (simtool={simtool})")
    print(f"{'='*60}")

    try:
        # Create a query object - this automatically fetches the schema
        query = results.query(tool_name, simtool=simtool)

        # Get schema using the .schema() method
        fields = query.schema()

        if not fields:
            print("No schema found.")
            return

        # Separate inputs and outputs
        inputs = [f for f in fields if f.startswith('input.')]
        outputs = [f for f in fields if f.startswith('output.')]

        print(f"\nFound {len(inputs)} input fields and {len(outputs)} output fields.")

        print("\n--- INPUT FIELDS ---")
        for field in inputs:
            # Remove 'input.' prefix for cleaner display
            print(f"  - {field[6:]}")

        print("\n--- OUTPUT FIELDS ---")
        for field in outputs:
            # Remove 'output.' prefix for cleaner display
            print(f"  - {field[7:]}")

    except Exception as e:
        print(f"Error fetching schema: {e}")

# Initialize session
# Note: You need a valid token for this to work
auth_data = {
    "grant_type": "personal_token",
    "token": "YOUR_TOKEN_HERE" 
}

print("Connecting to nanoHUB API...")
session = Session(auth_data, url="https://nanohub.org/api")
results = Results(session)

# Example 1: Inspect a simulation tool
print_schema("st4pnjunction", simtool=True)

# Example 2: Inspect a Rappture tool
print_schema("2dfets", simtool=False)
