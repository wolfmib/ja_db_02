# ja_db_02
Use Docker and CICD Git-Hub Actions

# install docker
# mac ( the other command in linux may vary, please note)

brew install -cast docker


# install docker-compose
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-darwin-aarch64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose


# setup yaml
see files

# run docker-compose 
docker compose up -d



# enter the docker-db with custom target tables

- docker exec -it ja_db_02-db-1 psql -U ja_admin -d ja_clients
- source docker_enter_jadb-02.sh
