# TEA: Telos EVM Ansible

Setup/Manage Telos EVM nodes using this ansible playbook!

## quickstart

### config

First copy one of the templates:

 - `cp config.local.yml config.yml` - for local private test chain with everything deployed (ideal for tests!)
 - `cp config.mainnet.yml config.yml` - telos mainnet evm node
 - `cp config.testnet.yml config.yml` - telos testnet evm node (WIP)

All configuration is done though `config.yml`, some parameters to have in mind:

 - `node_name`: alias for this noe

By default `testnet` & `mainnet` nodes are read-only, set `reth.sign_*` settings to be able to execute EVM transactions using the RPC endpoint.

### requires

 - `docker`
 - `python3`

### usage

    bash install.sh  # this will install uv pkg manager if not found

    uv run ansible-playbook tea_up.yml --ask-become-pass
    uv run ansible-playbook tea_down.yml --ask-become-pass

