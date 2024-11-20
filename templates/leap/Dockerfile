from --platform=linux/amd64 ubuntu:22.04

env DEBIAN_FRONTEND=noninteractive

run apt-get update && \
    apt-get install \
        -y \
        --no-install-recommends \
        git \
        wget \
        zstd \
        binutils \
        ca-certificates

# install snapshots from latest evm deployments
workdir /
run wget http://storage.telos.net/test-resources/telos-mainnet-snapshot-evm-deploy.bin
# run wget http://storage.telos.net/test-resources/telos-testnet-snapshot-evm-deploy.bin

# install nodeos
workdir /root
run wget https://github.com/AntelopeIO/leap/releases/download/v5.0.3/leap_5.0.3_amd64.deb && \
   apt-get install -y -f ./leap_5.0.3_amd64.deb

copy logging.json /root/logging.json
