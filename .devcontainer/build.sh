
[ ! -f .env ] || export $(grep -v '^#' .env | xargs)

echo "Using following container name: "$GAUSSIAN_SPLATTING_DOCKER_NAME

cd ..
docker build -t $GAUSSIAN_SPLATTING_DOCKER_NAME  . -f .devcontainer/Dockerfile
docker push $GAUSSIAN_SPLATTING_DOCKER_NAME