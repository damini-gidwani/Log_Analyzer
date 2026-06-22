#!/bin/bash
set -e  #stop the script if any cmd fails
echo "starting log Analyzer deployment...."
echo "stopping old containers.."
docker compose down
echo "building docker images.."
docker compose build
echo "starting containers.."
docker compose up -d
echo "running containers : "
docker ps
echo "container logs : "
docker compose logs -f
