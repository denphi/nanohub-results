from nanohubremote import Session
from nanohubresults import Results

# Initialize session with authentication
# Replace with your actual token from https://nanohub.org/developer
auth_data = {
    "grant_type": "personal_token",
    "token": "YOUR_TOKEN_HERE"
}
session = Session(auth_data, url="https://nanohub.org/api")
results = Results(session)

# Advanced filtering with multiple conditions and sorting
# Search for '2dfets' tool results
# Filter: Fermi energy between 0.2 and 0.4V
# Filter: Gate length > 15nm
# Sort by Fermi energy in descending order
print("Building query with multiple filters and sorting...")
query = results.query("2dfets", simtool=False) \
    .filter("input.Ef", ">", 0.2) \
    .filter("input.Ef", "<", 0.4) \
    .filter("input.Lg", ">", 15) \
    .select("input.Ef", "input.Lg", "input.temperature", "output.f11") \
    .sort("input.Ef", asc=False) \
    .limit(20) \
    .offset(0)

print("Executing query...")
response = query.execute()

print(f"\nNumber of results: {len(response.get('results', []))}")
print(f"Search time: {response.get('searchTime', 0)} seconds")

# Display first 3 results
if response.get('results'):
    print("\nFirst 3 results:")
    for i, result in enumerate(response['results'][:3]):
        print(f"\nResult {i+1}:")
        print(f"  SQUID: {result.get('squid')}")
        print(f"  Fermi Energy: {result.get('input.Ef')} V")
        print(f"  Gate Length: {result.get('input.Lg')} nm")
        print(f"  Temperature: {result.get('input.temperature')}")
