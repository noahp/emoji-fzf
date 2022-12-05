
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
RUN git clone --branch v2.3.7 https://github.com/pyenv/pyenv.git /pyenv
ENV PYENV_ROOT /pyenv
RUN /pyenv/bin/pyenv install 3.7.15
RUN /pyenv/bin/pyenv install 3.8.15
RUN /pyenv/bin/pyenv install 3.9.15
RUN /pyenv/bin/pyenv install 3.10.8
RUN /pyenv/bin/pyenv install 3.11.0

ENV PATH=/pyenv/bin:${PATH}

# Python requirements
RUN pip3 install --no-cache-dir \
    tox==3.26.0 \
    tox-pyenv==1.1.0
