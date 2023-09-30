import os
import sys

import anyio

import dagger


async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        
        # get reference to source code directory
        entries = await client.host().directory(".", exclude=["ci", ".venv"]).entries()

        print(entries)


anyio.run(main)