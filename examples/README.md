# nanohub-results Examples

This directory contains examples of how to use the `nanohub-results` library.

## 📓 Jupyter Notebooks (Recommended)

Interactive notebooks with comprehensive documentation and examples:

### [01_basic_search.ipynb](01_basic_search.ipynb)
**Getting Started with nanoHUB Results**
- Authentication with the nanoHUB API
- Exploring tool schemas
- Building and executing basic queries
- Accessing result data
- Optional visualization examples

### [02_advanced_filtering.ipynb](02_advanced_filtering.ipynb)
**Advanced Query Techniques**
- Multiple filter conditions (AND logic)
- All available filter operations (=, !=, >, <, >=, <=, like, in)
- Sorting results (ascending/descending)
- Manual pagination with offset/limit
- Verifying query results

### [03_downloading_files.ipynb](03_downloading_files.ipynb)
**Working with Result Data**
- Accessing curve data and scalar values
- Saving data to JSON and CSV formats
- Batch data processing
- Converting to pandas DataFrames
- Data visualization with matplotlib

### [04_pagination.ipynb](04_pagination.ipynb)
**Handling Large Result Sets**
- Automatic pagination with `paginate()`
- Manual pagination techniques
- Batch processing strategies
- Collecting statistics efficiently
- Performance optimization tips

## 🐍 Python Scripts

Standalone Python scripts for quick reference:
- `01_basic_search.py` - Basic search example
- `02_advanced_filtering.py` - Advanced filtering and sorting
- `03_downloading_files.py` - Accessing and saving result data
- `04_pagination.py` - Pagination example

## Getting Started

### Prerequisites

```bash
pip install nanohub-results nanohubremote
```

For full notebook functionality:
```bash
pip install jupyter matplotlib pandas
```

### Authentication

All examples require a nanoHUB API token. Get yours at:
**https://nanohub.org/developer**

Replace `YOUR_TOKEN_HERE` in the examples with your actual token.

**Security Note:** Never commit your token to version control. Consider using environment variables:

```python
import os
auth_data = {
    "grant_type": "personal_token",
    "token": os.environ.get("NANOHUB_TOKEN")
}
```

## Running the Examples

### Jupyter Notebooks
```bash
cd examples
jupyter notebook
# Open any .ipynb file
```

### Python Scripts
```bash
cd examples
python 01_basic_search.py
```

## Example Workflow

1. **Start with basics** → `01_basic_search.ipynb`
2. **Learn advanced queries** → `02_advanced_filtering.ipynb`
3. **Work with data** → `03_downloading_files.ipynb`
4. **Scale up** → `04_pagination.ipynb`

## Need Help?

- Check the [main README](../README.md)
- Review the [API documentation](../docs/)
- Open an issue on GitHub
