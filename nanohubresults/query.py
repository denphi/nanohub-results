#  Copyright 2025 HUBzero Foundation, LLC.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

#  HUBzero is a registered trademark of Purdue University.

#  Authors:
#  Daniel Mejia (denphi), Purdue University (denphi@denphi.com)

import json


class Query:
    VALID_OPERATIONS = {'=', '!=', '>', '<', '>=', '<=', 'like', 'in'}

    def __init__(self, library, tool, simtool=False):
        """
        Initialize a Query builder.
        
        Args:
            library: Instance of Results library.
            tool (str): Name of the tool to search.
            simtool (bool): Whether this is a simulation tool.
        """
        self.library = library
        self.tool = tool
        self._filters = []
        self._results_fields = []
        self._limit = 50
        self._offset = 0
        self._revision = 0
        self._valid_runs = True
        self._simtool = simtool
        self._sort = ""
        self._sort_asc = True
        self._random = False
        
        self._valid_fields = self._fetch_valid_fields()

    def _fetch_valid_fields(self):
        """
        Fetch valid input/output fields for the tool.
        
        Returns:
            set: Set of valid field names (e.g., 'input.field1', 'output.result1')
            
        Raises:
            ValueError: If tool schema cannot be fetched or tool doesn't exist
        """
        try:
            response = self.library.get_tool_detail(self.tool, simtool=self._simtool)
            
            if not response.get('success'):
                raise ValueError(
                    f"Failed to fetch schema for tool '{self.tool}'. "
                    f"Please verify the tool name is correct and try again."
                )
            
            if not response.get('results'):
                raise ValueError(
                    f"Tool '{self.tool}' not found or has no schema. "
                    f"Please verify the tool name and simtool parameter."
                )
            
            tool_data = response['results'][0].get(self.tool)
            if not tool_data:
                raise ValueError(
                    f"Tool '{self.tool}' schema is empty or malformed."
                )
                
            inputs = tool_data.get('input', {}).keys()
            outputs = tool_data.get('output', {}).keys()
            
            valid_fields = set()
            for k in inputs:
                valid_fields.add(f"input.{k}")
            for k in outputs:
                valid_fields.add(f"output.{k}")
            
            if not valid_fields:
                raise ValueError(
                    f"Tool '{self.tool}' has no input or output fields defined."
                )
                
            return valid_fields
            
        except KeyError as e:
            raise ValueError(
                f"Error parsing schema for tool '{self.tool}': {str(e)}"
            )
        except Exception as e:
            # If it's already a ValueError we raised, re-raise it
            if isinstance(e, ValueError):
                raise
            # For other exceptions (network errors, etc.), provide helpful message
            raise ValueError(
                f"Unable to fetch schema for tool '{self.tool}': {str(e)}. "
                f"Please check your connection and tool name."
            )


    def filter(self, field, op, value):
        """
        Add a filter condition.
        
        Args:
            field (str): Field name (e.g., 'output.energy').
            op (str): Operation (e.g., '=', '>', '<', 'like').
            value: Value to compare against.
            
        Returns:
            Query: Self for chaining.
            
        Raises:
            ValueError: If field or op is invalid.
        """
        if op not in self.VALID_OPERATIONS:
            raise ValueError(f"Invalid operation '{op}'. Valid operations are: {self.VALID_OPERATIONS}")
        
        # Validate field against tool schema (_valid_fields is always populated)
        if field not in self._valid_fields:
            raise ValueError(
                f"Invalid field '{field}' for tool '{self.tool}'. "
                f"Available fields: {sorted(list(self._valid_fields))}"
            )


        self._filters.append({
            "field": field,
            "operation": op,
            "value": value
        })
        return self

    def select(self, *fields):
        """
        Specify fields to return in the results.
        
        Args:
            *fields: Variable number of field names.
            
        Returns:
            Query: Self for chaining.
            
        Raises:
            ValueError: If any field is invalid.
        """
        for field in fields:
            # Validate field against tool schema (_valid_fields is always populated)
            if field not in self._valid_fields:
                raise ValueError(
                    f"Invalid field '{field}' for tool '{self.tool}'. "
                    f"Available fields: {sorted(list(self._valid_fields))}"
                )

        self._results_fields.extend(fields)
        return self

    def limit(self, limit):
        """Set the maximum number of results."""
        self._limit = limit
        return self

    def offset(self, offset):
        """Set the number of results to skip."""
        self._offset = offset
        return self

    def revision(self, revision):
        """Set the tool revision number."""
        self._revision = revision
        return self
        
    def valid_runs(self, valid=True):
        """Filter for valid runs only."""
        self._valid_runs = valid
        return self
        
    def simtool(self, is_simtool=True):
        """
        Filter for simulation tools.
        
        Note: Changing this after initialization might invalidate the schema validation 
        if the tool schema depends on this flag (though usually tool name is unique).
        """
        self._simtool = is_simtool
        return self

    def sort(self, field, asc=True):
        """Set the sort order."""
        # Validate field against tool schema (_valid_fields is always populated)
        if field not in self._valid_fields:
            raise ValueError(
                f"Invalid sort field '{field}' for tool '{self.tool}'. "
                f"Available fields: {sorted(list(self._valid_fields))}"
            )

        self._sort = field
        self._sort_asc = asc
        return self
        
    def random(self, random=True):
        """Return results in random order."""
        self._random = random
        return self

    def execute(self):
        """
        Execute the search query.
        
        Returns:
            dict: Search results.
            
        Raises:
            ValueError: If no filters have been added to the query.
        """
        if not self._filters:
            raise ValueError(
                "At least one filter is required. The API requires at least one filter condition. "
                "Use .filter(field, operation, value) to add a filter before calling execute()."
            )
        
        return self.library.search(
            tool=self.tool,
            filters=self._filters,
            results_fields=self._results_fields,
            limit=self._limit,
            offset=self._offset,
            revision=self._revision,
            valid_runs=self._valid_runs,
            simtool=self._simtool,
            sort=self._sort,
            sort_asc=self._sort_asc,
            random=self._random
        )

    def paginate(self, per_page=50):
        """
        Iterate over all results using pagination.
        
        Args:
            per_page (int): Number of results per page.
            
        Yields:
            dict: Individual result items.
            
        Raises:
            ValueError: If no filters have been added to the query.
        """
        if not self._filters:
            raise ValueError(
                "At least one filter is required. The API requires at least one filter condition. "
                "Use .filter(field, operation, value) to add a filter before calling paginate()."
            )
        
        current_offset = self._offset
        # We don't want to modify the builder's state permanently, 
        # but we need to iterate.
        # Let's keep the original offset and limit to restore later if needed,
        # or just use local variables for the loop.
        
        while True:
            # Execute search with current offset and limit
            response = self.library.search(
                tool=self.tool,
                filters=self._filters,
                results_fields=self._results_fields,
                limit=per_page,
                offset=current_offset,
                revision=self._revision,
                valid_runs=self._valid_runs,
                simtool=self._simtool,
                sort=self._sort,
                sort_asc=self._sort_asc,
                random=self._random
            )

            # Check if we got results (API may return error codes or empty results)
            if not response.get('results') or response.get('code') == 404:
                break

            results = response['results']
            for result in results:
                yield result
                
            if len(results) < per_page:
                break
                
            current_offset += per_page
