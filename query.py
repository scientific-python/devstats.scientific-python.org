import os
import requests
import json

class QueryClient(object):
    """
    Base class for github graphql query.
    """
    def __init__(self):
        # Make sure token is set
        try:
            self.token = os.environ['GRAPH_API_KEY']
        except KeyError:
            raise ValueError((
                "GRAPH_API_KEY not found in environment variables. "
                "Run $export GRAPH_API_KEY=<your access token> to access "
                "the GitHub GraphQL API"
                ))

if __name__ == "__main__":
    client = QueryClient()
