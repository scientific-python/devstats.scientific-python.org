from setuptools import setup, find_packages

# Grab long description from README
with open("README.md") as fh:
    long_description = fh.read()

def _get_reqs(fname):
    """
    Load requirements.txt file into a list.
    """
    with open(fname, 'r') as fh:
        reqs = [r for r in fh.read().split('\n') if not r.startswith('#')]
    return reqs

# Dependencies

setup(
    name="gh-issues-explorer",
    version="0.0.1-dev",
    description=(
        "A package for exploring GitHub issues using the GraphQL API."
    ),
    long_description=long_description,
    url="https://github.com/rossbar/github_graphql",
    author="rossbar",
    author_email="rossbar@berkeley.edu",
    license="BSD-3",
    packages=find_packages(),
    python_requires=">=3.6",    # For f-strings
    install_requires=_get_reqs("requirements.txt"),
    extras_require={
        "docs" : _get_reqs("doc/requirements.txt"),
    }
)
