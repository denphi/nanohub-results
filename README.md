# nanohub-results

Python library to interact with the NanoHUB Results API. This library provides a Pythonic interface for searching, filtering, and downloading simulation results from NanoHUB tools.

## Features

- **Pythonic Query Builder**: Fluent interface with method chaining
- **Field Validation**: Automatic validation against tool schemas
- **Operation Validation**: Only valid operations (`=`, `!=`, `>`, `<`, `>=`, `<=`, `like`, `in`)
- **Pagination**: Automatic iteration over large result sets
- **Complete API Coverage**: Access to all dbexplorer and download endpoints

## Installation

```bash
cd nanohub-results
pip install .
```

## Quick Start

```python
import nanohubremote as nr
from nanohubresults import Results

# Initialize session with authentication
auth_data = {
    "grant_type": "personal_token",
    "token": "your_token_here"
}
session = nr.Session(auth_data, url="https://nanohub.org/api")
results = Results(session)

# Get list of available tools
tools = results.get_tools(simtool=False)
print(tools)

# Search for results using the Query builder
response = results.query("2dfets") \
    .filter("output.Id", ">", 1e-6) \
    .select("output.Id", "output.Vt") \
    .limit(10) \
    .execute()

print(response)
```

## Available Tools

Some example tools available on NanoHUB:

**Rappture Tools:**
- `2dfets` - 2D FET I-V characteristics simulator
- `1dphononbte` - 1D Phonon BTE Solver for heat transport
- `abinit` - DFT calculations for molecules and periodic solids
- `1dchainmd` - 1D Chain Dispersions
- `1dfdmht` - 1D Finite Different Method Heat Transfer
- `2dmatstacks` - Electrostatic Properties of Layered 2D Materials
- `adept` - Solar cell and semiconductor device modeling
- `advte` - Advanced Thermoelectric Power Generation

**Sim2L Tools:**
- `alphafold231` - AlphaFold 2.3.1 protein structure prediction
- `cellrelaxdft` - Cell Relax DFT calculations
- `elasticdft` - Elastic Constants with DFT
- `gaussianthermo` - First-Principles Thermochemical Dataset

> [!NOTE]
> **Rappture vs Sim2L Tools**: Rappture tools use `simtool=False` (default), while Sim2L tools require `simtool=True`.

## Usage Examples

### 1. List Available Tools

```python
# Get all simulation tools
tools = results.get_tools(simtool=True)
for tool in tools['results']:
    print(f"{tool['tool_name']}: {tool['title']}")
```

### 2. Get Tool Schema

```python
# Get detailed schema for a tool
schema = results.get_tool_detail("2dfets")
print(schema)
```

### 3. Search with Filters

```python
# Search with multiple filters
query = results.query("1dphononbte") \
    .filter("input.acoustic_length", ">", 1) \
    .filter("output.temperature", ">", 300) \
    .select("input.acoustic_length", "output.temperature", "output.heat_flux") \
    .sort("output.temperature", asc=True) \
    .limit(20)

response = query.execute()
```

### 4. Pagination

```python
# Iterate over all results
for result in results.query("abinit") \
        .filter("output.energy", "<", 0) \
        .select("output.energy", "output.forces") \
        .paginate(per_page=50):
    print(result)
```

### 5. Download Files

```python
# Download a specific output field
file_content = results.download(
    tool="abinit",
    squid="simulation_id_here",
    field="output.wavefunction"
)

with open("wavefunction.dat", "wb") as f:
    f.write(file_content)
```

## Testing Without Installation

All examples include path configuration for testing without installation:

```bash
cd examples
python3 01_basic_search.py
```

## API Reference

### Results Class

#### `query(tool, simtool=False)`
Create a Query builder for a tool.

#### `get_tools(simtool=False, description_active=False)`
Get list of available tools.

#### `get_tool_detail(tool, revision=0, simtool=False)`
Get tool schema and metadata.

#### `search(tool, filters, results_fields, ...)`
Direct search (or use Query builder).

#### `download(tool, squid, field=None, ...)`
Download files or output fields.

### Query Class

Methods (all return `self` for chaining):
- `filter(field, op, value)` - Add filter condition
- `select(*fields)` - Specify fields to return
- `limit(limit)` - Set result limit
- `offset(offset)` - Set pagination offset
- `sort(field, asc=True)` - Set sort order
- `execute()` - Execute the query
- `paginate(per_page=50)` - Iterate over all results

## Valid Operations

- `=` - Equal
- `!=` - Not equal
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `like` - Pattern matching
- `in` - In list

## Examples Directory

See the `examples/` directory for complete examples:
- `01_basic_search.py` - Basic query usage
- `02_advanced_filtering.py` - Multiple filters and sorting
- `03_downloading_files.py` - File downloads
- `04_pagination.py` - Automatic pagination

## License

See LICENSE file for details.
