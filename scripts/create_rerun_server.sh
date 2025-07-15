set -a; source ../.env; set +a

IMAGE_NAME=drawsever
CONTAINER_NAME="drawserver"
NETWORK_NAME="mynetwork2"

# Check if the network exists
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  echo "Creating Docker network: $NETWORK_NAME"
  docker network create "$NETWORK_NAME"
else
  echo "Docker network '$NETWORK_NAME' already exists."
fi

if [ "$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "Starting '$CONTAINER_NAME'."
  docker start "$CONTAINER_NAME"
else
  echo "Container '$CONTAINER_NAME' does not exist. Creating it. "
  docker build .. -t $IMAGE_NAME
  docker run -d \
    --name $CONTAINER_NAME \
    -p 8005:80 \
    --network $NETWORK_NAME \
    $IMAGE_NAME
fi
