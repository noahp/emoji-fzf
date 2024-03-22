
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    clang \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    # python3-pip is used to install tox for orchestrating tests; the actual
    # test python environments are run via pyenv
    python3-pip \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# pyenv
COPY .python-version /tmp/.python-version
RUN git clone https://github.com/pyenv/pyenv.git /pyenv && cd /pyenv && git checkout 7e550e31f749ce3cda067644de44b18be761470b
ENV PYENV_ROOT /pyenv
RUN /pyenv/bin/pyenv install --skip-existing $(tr '\n' ' ' < /tmp/.python-version)

ENV PATH=/pyenv/bin:${PATH}

# Python requirements
RUN pip3 install --no-cache-dir \
    tox==3.28.0 \
    tox-pyenv==1.1.0
