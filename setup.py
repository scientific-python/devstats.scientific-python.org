from setuptools import setup, find_packages

# Grab long description from README
with open("README.md") as fh:
    long_description = fh.read()

# Dependencies
with open("requirements.txt") as fh:
    reqs = [
        req for req in fh.read().split('\n') if not req.startswith('#')
    ]

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
    install_requires=reqs,
)
