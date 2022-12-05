#!/usr/bin/env bash

# Simple test script to run the tests in docker

# Error on any non-zero command, and print the commands as they're run
set -ex

# Make sure we have the docker utility
if ! command -v docker; then
    echo "🐋 Please install docker first 🐋"
    exit 1
fi

GIT_ROOT_DIR=$(git worktree list | head -n1 | cut -d ' ' -f 1)

DOCKER_IMAGE_NAME="ghcr.io/noahp/emoji-fzf:latest"

# execute tox in the docker container.
# run tox in serial mode (omitting --parallel flag) because of this issue:
# when we test setup.py bdist_wheel, it writes to the .eggs directory. i'm
# not sure if there's a workaround for this
docker run --rm \
    --volume "$(pwd)":/mnt/workspace \
    --volume "${GIT_ROOT_DIR}":"${GIT_ROOT_DIR}" \
    -t "$DOCKER_IMAGE_NAME" bash -c "
    cp -r /mnt/workspace /tmp/workspace &&
    cd /tmp/workspace &&
    TOX_PARALLEL_NO_SPINNER=1 tox #--parallel
    "
