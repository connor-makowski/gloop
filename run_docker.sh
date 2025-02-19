docker build . --tag "gloop" --quiet > /dev/null
docker run -it --rm \
    --volume "$(pwd):/app" \
    --entrypoint /bin/bash \
    "gloop"

