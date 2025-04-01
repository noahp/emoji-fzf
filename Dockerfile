
FROM ubuntu:24.04

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
RUN git clone https://github.com/pyenv/pyenv.git /pyenv && cd /pyenv && git checkout d64d1aa1e0fa410e58cc218e721eb4c3672ce5bd
ENV PYENV_ROOT=/pyenv
RUN /pyenv/bin/pyenv install --skip-existing $(tr '\n' ' ' < /tmp/.python-version)

ENV PATH=/pyenv/bin:${PATH}

# Install uv for setting up test environment
COPY --from=ghcr.io/astral-sh/uv:0.6.11 /uv /uvx /bin/
