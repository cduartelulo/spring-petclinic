import os
import sys

import anyio

import dagger


async def main():
    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        
        # create a cache volume for Maven downloads
        maven_cache = client.cache_volume("gradle-cache")

        # get reference to source code directory
        source = client.host().directory(".", exclude=["ci", ".venv"])

        print(source)


anyio.run(main)