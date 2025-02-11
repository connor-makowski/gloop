docker build . --tag "gloop" --quiet
docker run -it --rm \
    --volume "$(pwd):/app" \
    "gloop"

