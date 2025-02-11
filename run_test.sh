docker build . --tag "gloop" --quiet > /dev/null
docker run -it --rm \
    --volume "$(pwd):/app" \
    "gloop"

