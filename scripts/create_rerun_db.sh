set -a; source ../.env; set +a

CONTAINER_NAME="my-postgres"
NETWORK_NAME="mynetwork2"

# Check if the network exists
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  echo "Creating Docker network: $NETWORK_NAME"
  docker network create "$NETWORK_NAME"
else
  echo "Docker network '$NETWORK_NAME' already exists."
fi

if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "Strating '$CONTAINER_NAME'."
  docker start "$CONTAINER_NAME"
else
  echo "Container '$CONTAINER_NAME' does not exist. Creating it. "
  docker run -d \
    --name $CONTAINER_NAME \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -v ${DB_LOCALPATH}:/var/lib/postgresql/data \
    -p 5432:${DB_PORT} \
    --network $NETWORK_NAME \
    postgres:17
fi
