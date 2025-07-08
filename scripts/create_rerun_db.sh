set -a; source ../.env; set +a

CONTAINER_NAME="my-postgres"
NETWORK_NAME="my-network"

# Check if the network exists
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  echo "Creating Docker network: $NETWORK_NAME"
  docker network create "$NETWORK_NAME"
else
  echo "Docker network '$NETWORK_NAME' already exists."
fi
docker network create my-network

if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
  docker start "$CONTAINER_NAME"
else
  echo "Container '$CONTAINER_NAME' does not exist."
  docker run -d \
    --name $CONTAINER_NAME \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -v ${DB_LOCALPATH}:/var/lib/postgresql/data \
    -p 5432:${DB_PORT} \
    --network my-network \
    postgres:17
fi
