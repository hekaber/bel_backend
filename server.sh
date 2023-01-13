#!/usr/bin/env bash

cat <<EOF
###############
Local Utilities
###############
EOF

usage() {
    cat <<EOF
Usage: server [params]
Params:
-s     | --start: start docker-compose
-n     | --stop: stop docker
-k     | --kill: reset image with image name param
EOF
}

killImage() {
    docker images --format="{{.Repository}} {{.ID}}" | 
    grep "^$1 " | 
    cut -d' ' -f2 | 
    xargs docker rmi
}

while [ "$1" != "" ]; do
  case $1 in
  -s | --start)
    # sync the solidity contract abi into the webapp
    docker-compose up --remove-orphans -d
    ;;
  -n | --stop)
    docker-compose down
    ;;
  -rmd | --remove-dangling)
    docker rmi $(docker images -f "dangling=true" -q)
    ;;
  -k | --kill)
    shift
    killImage $1
    ;;
  -cip | --container-ip)
    shift
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $1
    ;;
  -h | --help)
    usage
    exit
    ;;
  esac
  shift
done
