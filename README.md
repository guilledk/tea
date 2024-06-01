# TEA: Telos EVM Ansible

Setup/Manage Telos EVM nodes using this ansible playbook!

## quickstart

### config

First copy one of the templates:

 - `cp config.local.yml config.yml` - for local private test chain with everything deployed (ideal for tests!)
 - `cp config.mainnet.yml config.yml` - telos mainnet evm node
 - `cp config.testnet.yml config.yml` - telos testnet evm node

All configuration is done though `config.yml`, some parameters to have in mind:

 - `node_name`: alias for this noe
 - `rpc.host` & `rpc.ws_host` - Set these to `0.0.0.0` if you want to server trafic from the outside world

By default `testnet` & `mainnet` nodes are read-only, set `rpc.signer_*` settings to be able to execute EVM transactions using the RPC endpoint.

### requires

 - `docker`
 - `python3`

### usage

    bash install.sh
    source activate.sh
    ansible-playbook tea_up.yml --ask-become-pass
    ansible-playbook tea_down.yml --ask-become-pass

