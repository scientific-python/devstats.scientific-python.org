# GitHub GraphQL API

Notes from experimenting with GitHub's GraphQL API

## OAuth key for accessing GitHub

Per the [GitHub GraphQL API docs](https://developer.github.com/v4/guides/forming-calls/),
you need a personal access token to access the GraphQL API.

This code expects the personal access token to be in the environment variable
`GRAPH_API_KEY`.

You can [create a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) on GitHub and save it somewhere you trust.
Then, when you want to use the code: `export GRAPH_API_KEY=<yourkey>`
