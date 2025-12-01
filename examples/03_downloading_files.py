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

# First, let's get a real SQUID from the pntoy simulation tool
print("Fetching a sample result from pntoy (simulation tool)...")
query = results.query("pntoy", simtool=True) \
    .limit(1)

response = query.execute()

if response.get('results') and len(response['results']) > 0:
    sample_result = response['results'][0]
    squid = sample_result['squid']
    print(f"Found SQUID: {squid}")

    # Get list of available files for this SQUID
    print("\nFetching list of available files for this SQUID...")
    try:
        files_response = results.get_squid_files(squid, simtool=True)
        if files_response.get('results'):
            print(f"\nFound {files_response.get('total_files', 0)} file(s):")
            for file_info in files_response['results']:
                size_kb = file_info.get('size', 0) / 1024
                print(f"  - {file_info.get('name')} (ID: {file_info.get('id')}, Size: {size_kb:.2f} KB)")

            # Download the first file as an example
            first_file = files_response['results'][0]
            file_name = first_file.get('name')
            print(f"\nDownloading sample file: {file_name}")

            try:
                download_response = results.download(
                    tool="pntoy",
                    squid=squid,
                    file_name=file_name,
                    simtool=True
                )

                # Save the downloaded file
                output_filename = f"downloaded_{file_name}"

                import json
                if isinstance(download_response, dict):
                    with open(output_filename, 'w') as f:
                        json.dump(download_response, f, indent=2)
                    print(f"✓ File saved as JSON: {output_filename}")
                elif isinstance(download_response, bytes):
                    with open(output_filename, 'wb') as f:
                        f.write(download_response)
                    print(f"✓ File saved as binary: {output_filename}")
                else:
                    with open(output_filename, 'w') as f:
                        f.write(str(download_response))
                    print(f"✓ File saved: {output_filename}")

            except Exception as e:
                print(f"✗ Download failed: {e}")
        else:
            print("No downloadable files found for this SQUID.")
    except Exception as e:
        print(f"Could not retrieve file list: {e}")

    # Result data is also available directly from the search response
    print("\nNote: Result data is also available from the search response.")
    print(f"Available fields in result:")
    for key in sorted(sample_result.keys()):
        if key != 'squid':
            value = sample_result[key]
            if isinstance(value, dict) and 'xaxis' in value:
                print(f"  - {key}: curve data ({len(value['xaxis'])} points)")
            else:
                print(f"  - {key}: {value}")

    # Save the result data to a JSON file
    import json
    with open("pntoy_result_data.json", "w") as f:
        json.dump(sample_result, f, indent=2)
    print("\nComplete result saved to pntoy_result_data.json")

    # The download() method can be used for downloading actual files if available:
    # download_response = results.download("pntoy", squid, field="output.field_name", file_name="filename", simtool=True)
    # You can use the file IDs or names from get_squid_files() to download specific files.
else:
    print("No results found to download.")
