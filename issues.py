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


def send_query(query, cursor=None):
    """
    Helper function to use the graphql query example in `query_examples`
    to retrieve open numpy issues and all cross references
    """
    # Modifications to request template
    # TODO: Unhack this
    # WARNING: This hack relies on specific structure of issues query
    if cursor is not None:
        cursor_ind = query.find("issues(") + len("issues(")
        query = query[:cursor_ind] + f'after:"{cursor}", ' + query[cursor_ind:]
    # Build request payload
    payload = {'query' : ''.join(query.split('\n'))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)

def get_all_responses(query):
    """
    Helper function to bypass GitHub GraphQL API node limit.
    """
    # Get data from a single response
    initial_data = send_query(query)
    data, last_cursor, total_num_issues = parse_single_issue_query(initial_data)
    print("Retrieving {} out of {} values...".format(len(data), total_num_issues))
    # Continue requesting issues (with pagination) until all are acquired
    while len(data) < total_num_issues:
        rdata = send_query(query, cursor=last_cursor)
        pdata, last_cursor, _ = parse_single_issue_query(rdata)
        data.extend(pdata)
        print("Retrieving {} out of {} values...".format(len(data), total_num_issues))
    print("Done.")
    return data

def parse_single_issue_query(data):
    """
    Parse the raw json returned by get_open_numpy_issues_with_crossrefs.
    """
    try:
        total_num_issues = data['data']['repository']['issues']['totalCount']
        data = data['data']['repository']['issues']['edges']
        last_cursor = data[-1]['cursor']
    except KeyError as e:
        print(data)
        raise e
    return data, last_cursor, total_num_issues


class GithubIssueGrabber:
    """
    Pull down data via the GitHub APIv.4 given a valid GraphQL query.
    """

    def __init__(self, query_fname, repo_owner="numpy", repo_name="numpy"):
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
        repo_owner : str
            Repository owner. Default is "numpy"
        repo_name : str
            Repository name. Default is "numpy"
        """
        self.query_fname = query_fname
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
        self.raw_data = get_all_responses(self.query)

    def dump(self, outfile):
        """
        Dump raw json to `outfile`.
        """
        if not self.raw_data:
            raise ValueError("raw_data is currently empty, nothing to dump")

        with open(outfile, "w") as outf:
            json.dump(self.raw_data, outf)


if __name__ == "__main__":
    grabber = GithubIssueGrabber('query_examples/issue_activity_since_date.gql')
    grabber.get()
    grabber.dump("_data/issues.json")
