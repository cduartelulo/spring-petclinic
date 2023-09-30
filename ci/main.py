import os
import sys

import anyio

import dagger


async def main():
    # check for Docker Hub registry credentials in host environment
    # for var in ["DOCKERHUB_USERNAME", "DOCKERHUB_PASSWORD"]:
    #     if var not in os.environ:
    #         msg = f"{var} environment variable must be set"
    #         raise OSError(msg)

    # initialize Dagger client
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # username = os.environ["DOCKERHUB_USERNAME"]
        # # set registry password as secret for Dagger pipeline
        # password = client.set_secret("password", os.environ["DOCKERHUB_PASSWORD"])

        # create a cache volume for Maven downloads
        maven_cache = client.cache_volume("gradle-cache")

        # get reference to source code directory
        source = client.host().directory(".", exclude=["ci", ".venv"])

        # create database service container
        mariadb = (
            client.container()
            .from_("mariadb:10.11.2")
            .with_env_variable("MARIADB_USER", "petclinic")
            .with_env_variable("MARIADB_PASSWORD", "petclinic")
            .with_env_variable("MARIADB_DATABASE", "petclinic")
            .with_env_variable("MARIADB_ROOT_PASSWORD", "root")
            .with_exposed_port(3306)
            .with_exec([])
        )

        # use maven:3.9 container
        # mount cache and source code volumes
        # set working directory
        app = (
            client.container()
            .from_("gradle:7.6.1-jdk17")
            .with_mounted_cache("/root/.m2", maven_cache)
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
        )

        # define binding between
        # application and service containers
        # define JDBC URL for tests
        # test, build and package application as JAR
        build = (
            app.with_service_binding("db", mariadb)
            .with_env_variable(
                "MYSQL_URL",
                "jdbc:mysql://0.0.0.0:3306/petclinic",
            )
            .with_exec(["gradle", "-Dspring.profiles.active=mysql", "clean", "build"])
        )

        # use eclipse alpine container as base
        # copy JAR files from builder
        # set entrypoint and database profile
        deploy = (
            client.container()
            .from_("amazoncorretto:17.0.8")
            .with_directory("/app", build.directory("./build/libs"))
            .with_entrypoint(
                [
                    "java",
                    "-jar",
                    "-Dspring.profiles.active=mysql",
                    "/app/spring-petclinic-3.1.0.jar",
                ]
            )
        )
        

        # # publish image to registry
        # address = await deploy.with_registry_auth(
        #     "docker.io", username, password
        # ).publish(f"{username}/myapp")

        # # print image address
        # print(f"Image published at: {address}")

        version = await deploy.stdout()


anyio.run(main)