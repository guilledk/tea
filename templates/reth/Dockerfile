from rust:1-slim-bullseye

env DEBIAN_FRONTEND=noninteractive

run apt-get update && \
    apt-get install \
        -y \
        --no-install-recommends \
        git \
        pkg-config \
        libssl-dev \
        libclang-dev \
        build-essential \
        ca-certificates

workdir /

run git clone https://github.com/telosnetwork/telos-reth.git -b telos-v1.0.0-rc5

workdir /telos-reth

run bash build.sh

copy entrypoint.sh /entrypoint.sh

entrypoint ["/bin/bash", "/entrypoint.sh"]
