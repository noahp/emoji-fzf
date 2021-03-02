FROM ubuntu:focal

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    wget

# get user id from build arg, so we can have read/write access to directories
# mounted inside the container. only the UID is necessary, UNAME just for
# cosmetics
ARG UID=1010
ARG UNAME=builder

RUN useradd --uid $UID --create-home --user-group ${UNAME} && \
    echo "${UNAME}:${UNAME}" | chpasswd && adduser ${UNAME} sudo

USER ${UNAME}

# Install Conda
# Copied from continuumio/miniconda3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /home/${UNAME}/miniconda3/bin:/home/${UNAME}/.local/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b

# Install these in the base conda env
RUN pip3 install tox==3.22.0 tox-conda==0.7.1

WORKDIR /mnt/workspace
