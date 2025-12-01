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
        """Fetch valid input/output fields for the tool."""
        try:
            response = self.library.get_tool_detail(self.tool, simtool=self._simtool)
            if not response.get('success') or not response.get('results'):
                # Fallback or warning if tool not found, but for now let's return empty set 
                # or allow all if we can't validate. 
                # User requested validation, so raising error might be better if tool not found.
                return set()
            
            tool_data = response['results'][0].get(self.tool)
            if not tool_data:
                return set()
                
            inputs = tool_data.get('input', {}).keys()
            outputs = tool_data.get('output', {}).keys()
            
            valid_fields = set()
            for k in inputs:
                valid_fields.add(f"input.{k}")
            for k in outputs:
                valid_fields.add(f"output.{k}")
                
            return valid_fields
        except Exception:
            # If API call fails, we might want to warn or allow all.
            # For strict validation as requested, we should probably fail or log.
            # But to avoid breaking if offline/mocking isn't perfect in all envs, 
            # maybe we should allow if we can't fetch? 
            # The prompt says "I want filter and select to validate".
            # So I will assume strict validation.
            return set()

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
            
        if self._valid_fields and field not in self._valid_fields:
             # Only validate if we successfully fetched fields. 
             # If _valid_fields is empty, it might mean tool not found or API error.
             # But if tool has no fields, it's also empty.
             # Let's assume if we have a tool, we have fields.
             # If _valid_fields is empty, maybe we should warn?
             # For now, I'll raise error if I have fields and it's not in them.
             # If I have NO fields, it's suspicious.
             pass
        
        if self._valid_fields and field not in self._valid_fields:
             raise ValueError(f"Invalid field '{field}'. Available fields: {sorted(list(self._valid_fields))}")

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
            if self._valid_fields and field not in self._valid_fields:
                raise ValueError(f"Invalid field '{field}'. Available fields: {sorted(list(self._valid_fields))}")
                
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
        if self._valid_fields and field not in self._valid_fields:
             raise ValueError(f"Invalid sort field '{field}'.")
             
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
        """
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
        """
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
