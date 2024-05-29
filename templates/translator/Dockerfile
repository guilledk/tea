from node:18-bullseye

workdir /root

run git clone \
    https://github.com/telosnetwork/telosevm-translator.git \
    translator \
    -b v1.1.0

workdir /root/translator

run yarn build
