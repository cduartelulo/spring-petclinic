import sys

import anyio

import dagger


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # create a cache volume for Maven downloads
        maven_cache = client.cache_volume("maven-cache")

        # get reference to source code directory
        source = client.host().directory(".", include=["app"]).directory("app")
        
        app = (
            client
            .container()
            .from_("gradle:7.6.2-jdk17")
            .with_mounted_cache("/root/.m2", maven_cache)
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
        )

        build = (
            app
            .with_exec(["gradle", "clean", "build"])            
        )

        export = (
            build
            .directory(".")
            .export("./host")
        )

        await export
    

anyio.run(main)