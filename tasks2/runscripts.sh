#!/bin/bash/

echo "creating a docker network to enable visibility"
docker network create appnetwork --driver bridge
#build the haproxy container
docker build -t my-haproxy .
#run the container
docker run -d --name my-running-haproxy my-haproxy --network appnetwork -p 80:80
for i in {1..2}
do 
  echo "creating and running default nginx container"
  docker run --name mynginx"$i" -d nginx --network appnetwork
  echo "done"
done
