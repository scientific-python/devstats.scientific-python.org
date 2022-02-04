import os
import requests
import json

token = os.environ["GRAPH_API_KEY"]
endpoint = r"https://api.github.com/graphql"
headers = {"Authorization": "bearer {}".format(token)}


def load_query_from_file(fname, repo_owner="numpy", repo_name="numpy"):
    """
    Load an 'issue' query from file and set the target repository, where
    the target repository has the format:
    
    https://github.com/<repo_owner>/<repo_name>
    
    Parameters
    ----------
    fname : str
        Path to a text file containing a valid issue query according to the 
        GitHub GraphQL schema.
    repo_owner : str
        Owner of target repository on GitHub. Default is 'numpy'.
    repo_name : str
        Name of target repository on GitHub. Default is 'numpy'.
    
    Returns
    -------
    query : str
        Query loaded from file in text form suitable for ``send_query``.

    Notes
    -----
    This function expects the query to have a specific form and will not work
    for general GitHub GraphQL queries. See ``examples/`` for some valid
    templated issue queries.
    """
    with open(fname, "r") as fh:
        query = fh.read()
        # Set target repo from template
        query = query.replace("_REPO_OWNER_", repo_owner)
        query = query.replace("_REPO_NAME_", repo_name)
    return query


def send_query(query, query_type, cursor=None):
    """
    Send a GraphQL query via requests.post

    No validation is done on the query before sending. GitHub GraphQL is
    supported with the `cursor` argument.

    Parameters
    ----------
    query : str
        The GraphQL query to be sent
    query_type : {"issues", "pullRequests"}
        The object being queried according to the GitHub GraphQL schema.
        Currently only issues and pullRequests are supported
    cursor : str, optional
        If given, then the cursor is injected into the query to support
        GitHub's GraphQL pagination.

    Returns
    -------
    dict
        The result of the query (json) parsed by `json.loads`

    Notes
    -----
    This is intended mostly for internal use within `get_all_responses`.
    """
    # TODO: Expand this, either by parsing the query type from the query
    # directly or manually adding more query_types to the set
    if query_type not in {"issues", "pullRequests"}:
        raise ValueError(
            "Only 'issues' and 'pullRequests' queries are currently supported"
        )
    # TODO: Generalize this
    # WARNING: The cursor injection depends on the specific structure of the
    # query, this is the main reason why query types are limited to issues/PRs
    if cursor is not None:
        cursor_insertion_key = query_type + "("
        cursor_ind = query.find(cursor_insertion_key) + len(cursor_insertion_key)
        query = query[:cursor_ind] + f'after:"{cursor}", ' + query[cursor_ind:]
    # Build request payload
    payload = {'query' : ''.join(query.split('\n'))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)

def get_all_responses(query, query_type):
    """
    Helper function to bypass GitHub GraphQL API node limit.
    """
    # Get data from a single response
    initial_data = send_query(query, query_type)
    data, last_cursor, total_count = parse_single_query(initial_data, query_type)
    print(f"Retrieving {len(data)} out of {total_count} values...")
    # Continue requesting data (with pagination) until all are acquired
    while len(data) < total_count:
        rdata = send_query(query, query_type, cursor=last_cursor)
        pdata, last_cursor, _ = parse_single_query(rdata, query_type)
        data.extend(pdata)
        print(f"Retrieving {len(data)} out of {total_count} values...")
    print("Done.")
    return data

def parse_single_query(data, query_type):
    """
    Parse the data returned by `send_query`

    .. warning::
       
       Like `send_query`, the logic here depends on the specific structure
       of the query (e.g. it must be an issue or PR query, and must have a
       total count).
    """
    try:
        total_count = data['data']['repository'][query_type]['totalCount']
        data = data['data']['repository'][query_type]['edges']
        last_cursor = data[-1]['cursor']
    except KeyError as e:
        print(data)
        raise e
    return data, last_cursor, total_count


class GithubGrabber:
    """
    Pull down data via the GitHub APIv.4 given a valid GraphQL query.
    """

    def __init__(self, query_fname, query_type, repo_owner="numpy", repo_name="numpy"):
        """
        Create an object to send/recv queries related to the issue tracker
        for the given repository via the GitHub API v.4.

        The repository to query against is given by:
        https://github.com/<repo_owner>/<repo_name>

        Parameters
        ----------
        query_fname : str
            Path to a valid GraphQL query conforming to the GitHub GraphQL
            schema
        query_type : {"issues", "pullRequests"}
            Type of object that is being queried according to the GitHub GraphQL
            schema. Currently only "issues" and "pullRequests" are supported.
        repo_owner : str
            Repository owner. Default is "numpy"
        repo_name : str
            Repository name. Default is "numpy"
        """
        self.query_fname = query_fname
        self.query_type = query_type  # TODO: Parse this directly from query
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.raw_data = None
        self.load_query()

    def load_query(self):
        self.query = load_query_from_file(
            self.query_fname, self.repo_owner, self.repo_name
        )

    def get(self):
        """
        Get JSON-formatted raw data from the query.
        """
        self.raw_data = get_all_responses(self.query, self.query_type)

    def dump(self, outfile):
        """
        Dump raw json to `outfile`.
        """
        if not self.raw_data:
            raise ValueError("raw_data is currently empty, nothing to dump")

        with open(outfile, "w") as outf:
            json.dump(self.raw_data, outf)


if __name__ == "__main__":
    repo = "networkx"
    issues = GithubGrabber(
        'query_examples/issue_activity_since_date.gql',
        'issues',
        repo_owner=repo,
        repo_name=repo,
    )
    issues.get()
    issues.dump(f"_data/{repo}_issues.json")
    prs = GithubGrabber(
        'query_examples/pr_data_query.gql',
        'pullRequests',
        repo_owner=repo,
        repo_name=repo,
    )
    prs.get()
    prs.dump(f"_data/{repo}_prs.json")
