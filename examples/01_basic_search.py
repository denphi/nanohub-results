import nanohubremote as nr
from nanohubresults import Results

# Initialize session with authentication
# Replace with your actual token from https://nanohub.org/developer
auth_data = {
    "grant_type": "personal_token",
    "token": "YOUR_TOKEN_HERE"
}
session = nr.Session(auth_data, url="https://nanohub.org/api")

results = Results(session)

# Get the schema for 2dfets to see what fields are available
print("Getting tool schema for 2dfets...")
schema = results.get_tool_detail("2dfets", simtool=False)
print(f"Available input fields: {list(schema['results'][0]['2dfets']['input'].keys())[:5]}")
print(f"Available output fields: {list(schema['results'][0]['2dfets']['output'].keys())[:5]}")
print()

# Basic search using the Query builder
# Note: 2dfets is a Rappture tool, so simtool=False (default)
# For Sim2L tools like alphafold231, use simtool=True
# Search for '2dfets' tool results where Fermi energy > 0
# Select Fermi energy input and output curve f41
print("Executing query...")
query = results.query("2dfets", simtool=False) \
    .filter("input.Ef", ">", 0) \
    .select("input.Ef", "output.f41") \
    .limit(10)

response = query.execute()
print(f"Number of results: {len(response.get('results', []))}")
print(f"Search time: {response.get('searchTime', 0)} seconds")
print()

# Print the first result if available
if response.get('results') and len(response['results']) > 0:
    first_result = response['results'][0]
    print("First result:")
    print(f"  SQUID: {first_result.get('squid')}")
    print(f"  Fermi Energy: {first_result.get('input.Ef')}")
    print(f"  Output f41 data points: {len(first_result.get('output.f41', {}).get('xaxis', []))}")
