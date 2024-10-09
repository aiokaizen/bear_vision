#!/bin/bash

docker rm $(docker ps -aq)
docker volume rm $(docker volume ls -q)

# docker image rm $(docker images -aq)
# docker network rm $(docker network ls -q)
