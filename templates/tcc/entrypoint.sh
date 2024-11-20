#!/bin/bash

INSTALL_ROOT="$(pwd)"
CONSENSUS_BIN_PATH=$INSTALL_ROOT/target/release/telos-consensus-client

if [ ! -f $CONSENSUS_BIN_PATH ] || [ ! -x $CONSENSUS_BIN_PATH ]; then
    echo "Error: telos-consensus-client binary not found at $CONSENSUS_BIN_PATH\nHint: Did you run build.sh yet?"
    exit 1
fi

[ -f $INSTALL_ROOT/.env ] && . $INSTALL_ROOT/.env

[ -z "$CONSENSUS_CONFIG" ] && CONSENSUS_CONFIG=$INSTALL_ROOT/config.toml
[ -z "$LOG_PATH" ] && LOG_PATH=$INSTALL_ROOT/consensus.log

exec $CONSENSUS_BIN_PATH --config $CONSENSUS_CONFIG >> "$LOG_PATH" 2>&1
