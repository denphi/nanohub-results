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

# Use paginate() to iterate over all matching results
# This handles fetching pages automatically
print("Setting up pagination query for 2dfets tool...")
query = results.query("2dfets", simtool=False) \
    .filter("input.Ef", ">", 0) \
    .select("input.Ef", "input.Lg", "output.f11")

print("Iterating over results (fetching 10 per page):")
count = 0
for result in query.paginate(per_page=10):
    # Print a summary for each result
    if count < 5:  # Show details for first 5 only
        print(f"\nResult {count + 1}:")
        print(f"  SQUID: {result.get('squid')}")
        print(f"  Fermi Energy: {result.get('input.Ef')} V")
        print(f"  Gate Length: {result.get('input.Lg')} nm")
    elif count == 5:
        print("\n... (showing count only for remaining results)")

    count += 1
    if count >= 50:  # Safety break for example
        break

print(f"\nTotal results processed: {count}")
print("Note: The paginate() method automatically handles fetching multiple pages as needed.")
