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
        wget

# get user id from build arg, so we can have read/write access to directories
# mounted inside the container. only the UID is necessary, UNAME just for
# cosmetics
ARG UID=1010
ARG UNAME=builder

RUN useradd --uid $UID --create-home --user-group ${UNAME} && \
    echo "${UNAME}:${UNAME}" | chpasswd && adduser ${UNAME} sudo

USER ${UNAME}

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /home/${UNAME}/.local/bin:$PATH

# Install tox
RUN pip3 install tox==3.22.0

WORKDIR /mnt/workspace
