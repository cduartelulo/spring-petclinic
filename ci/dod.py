import sys

import anyio

import os

from github import Auth
from github import Github


async def main():
    auth = Auth.Token(os.environ.get('GITHUB_AUTH_TOKEN'))
    g = Github(auth=auth)
    repo = g.get_repo('cduartelulo/spring-petclinic')
    commit = repo.get_git_commit(sha=os.environ.get('CIRCLE_SHA1'))

    print('Hash commit:', commit.sha)

    print('Commit message:', commit.message)

    print('Committer date:', commit.committer.date)

async def print_env_vars():
    [print("Name:", name, "Value:", value) for name, value in os.environ.items()]

anyio.run(main)
anyio.run(print_env_vars)