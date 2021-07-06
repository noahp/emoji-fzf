# This docker image is pushed to noahpendleton/emoji-fzf and used in the
# Dockerfile

FROM ubuntu:focal

# Install the python versions
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && apt-get update && \
    apt-get install -y \
        git \
        python2.7 \
        python3 \
        python3-pip \
        python3.6 \
        python3.7 \
        python3.8 \
        python3.9 \
        python3.10 \
        wget

# Install tox. We need a version prior to 3.8 for python3.10 virtualenv to
# support running pip, see more info here:
# https://github.com/tox-dev/tox/issues/1485
#
# A better fix would be updating virtualenv to the correct upstream patched
# version, but I couldn't get it to work first try so I gave up
RUN python3 -m pip install 'tox<3.8'
