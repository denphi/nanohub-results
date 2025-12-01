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

import os
from urllib.parse import urlencode
from .query import Query

class Results:
    def __init__(self, session):
        """
        Initialize the Results library with a nanohubremote Session.
        
        Args:
            session: An instance of nanohubremote.Session
        """
        self.session = session
        self.base_api = "results"

    def query(self, tool, simtool=False):
        """
        Create a new Query builder for a tool.
        
        Args:
            tool (str): Name of the tool to search.
            simtool (bool): Whether this is a simulation tool.
            
        Returns:
            Query: A new Query instance.
        """
        return Query(self, tool, simtool=simtool)

    def get_tools(self, simtool=False, description_active=False):
        """
        Retrieve a list of available tools.
        
        Args:
            simtool (bool): Filter for simulation tools only.
            description_active (bool): Include tool descriptions.
            
        Returns:
            dict: API response containing list of tools.
        """
        params = {
            "simtool": "true" if simtool else "false",
            "description_active": "true" if description_active else "false"
        }
        url = f"{self.base_api}/dbexplorer/tools?{urlencode(params)}"
        return self.session.requestGet(url).json()

    def get_tool_detail(self, tool, revision=0, simtool=False):
        """
        Retrieve detailed information about a specific tool.

        Args:
            tool (str): Tool name identifier.
            revision (int): Tool revision number (0 for latest).
            simtool (bool): Filter for simulation tools.

        Returns:
            dict: API response containing tool details.
        """
        data = {
            "tool": tool
        }
        url = f"{self.base_api}/dbexplorer/tool_detail"
        return self.session.requestPost(url, data=data).json()

    def get_squid_detail(self, squid, output="json", simtool=False):
        """
        Retrieve detailed information about a specific simulation run (SQUID).
        
        Args:
            squid (str): Simulation unique identifier.
            output (str): Output format: 'json' or 'xml'.
            simtool (bool): Filter for simulation tools.
            
        Returns:
            dict/str: Simulation run details.
        """
        params = {
            "squid": squid,
            "output": output,
            "simtool": "true" if simtool else "false"
        }
        url = f"{self.base_api}/dbexplorer/squid_detail?{urlencode(params)}"
        return self.session.requestGet(url).json()

    def search(self, tool, filters, results_fields, limit=50, offset=0, revision=0, valid_runs=True, simtool=False, sort="", sort_asc=True, random=False):
        """
        Search tool simulation results with filters.

        Args:
            tool (str): Tool name to search.
            filters (list): List of filter objects.
            results_fields (list): List of result fields to return.
            limit (int): Maximum number of results.
            offset (int): Pagination offset.
            revision (int): Tool revision number.
            valid_runs (bool): Only include valid runs.
            simtool (bool): Filter for simulation tools.
            sort (str): Field name to sort by.
            sort_asc (bool): Sort in ascending order.
            random (bool): Return results in random order.

        Returns:
            dict: Search results.
        """
        data = {
            "tool": tool,
            "filters": json.dumps(filters),
            "results": json.dumps(results_fields),
            "limit": limit
        }

        # Only include optional parameters if they differ from defaults
        if offset != 0:
            data["offset"] = offset
        if revision != 0:
            data["revision"] = revision
        if not valid_runs:
            data["valid_runs"] = "false"
        if simtool:
            data["simtool"] = "true"
        if sort:
            data["sort"] = sort
            data["sort_asc"] = "true" if sort_asc else "false"
        if random:
            data["random"] = "true"

        url = f"{self.base_api}/dbexplorer/search"
        return self.session.requestPost(url, data=data).json()

    def stats(self, tool, filters, results_fields, limit=50, revision=0, valid_runs=True, simtool=False):
        """
        Get statistical information about tool results.

        Args:
            tool (str): Tool name to analyze.
            filters (list): List of filter objects.
            results_fields (list): List of result fields to include.
            limit (int): Maximum number of results.
            revision (int): Tool revision number.
            valid_runs (bool): Only include valid runs.
            simtool (bool): Filter for simulation tools.

        Returns:
            dict: Statistical summary.
        """
        data = {
            "tool": tool,
            "filters": json.dumps(filters),
            "results": json.dumps(results_fields),
            "limit": limit,
            "revision": revision,
            "valid_runs": "true" if valid_runs else "false",
            "simtool": "true" if simtool else "false"
        }
        url = f"{self.base_api}/dbexplorer/stats"
        return self.session.requestPost(url, data=data).json()

    def records(self, simtool=False):
        """
        Get database table record counts and search statistics.
        
        Args:
            simtool (bool): Filter for simulation tools.
            
        Returns:
            dict: Record counts and stats.
        """
        params = {
            "simtool": "true" if simtool else "false"
        }
        url = f"{self.base_api}/dbexplorer/records?{urlencode(params)}"
        return self.session.requestGet(url).json()

    def get_squid_files(self, squid, simtool=True):
        """
        Get list of files associated with a simulation run (SQUID).

        Args:
            squid (str): Simulation unique identifier.
            simtool (bool): Whether this is a simulation tool (default: True).
                           File listing only works for simulation tools.

        Returns:
            dict: API response containing list of files with id, name, and size.
        """
        data = {
            "squid": squid,
            "simtool": "true" if simtool else "false"
        }
        url = f"{self.base_api}/dbexplorer/squid_files"
        return self.session.requestPost(url, data=data).json()

    def download(self, tool, squid, field=None, file_name=None, complete=False, simtool=False):
        """
        Download simulation results, output files, or input parameters.

        Args:
            tool (str): Tool resource ID.
            squid (str): Simulation unique identifier.
            field (str): Field name or file ID to download.
            file_name (str): File name to download (alternative to field).
            complete (bool): Include only input fields (true) or both (false).
            simtool (bool): Filter for simulation tools.

        Returns:
            bytes: File content.
        """
        params = {
            "tool": tool,
            "squid": squid,
            "complete": "true" if complete else "false",
            "simtool": "true" if simtool else "false"
        }
        if field:
            params["field"] = field
        if file_name:
            params["file"] = file_name

        url = f"{self.base_api}/download?{urlencode(params)}"
        return self.session.requestGet(url).json()
