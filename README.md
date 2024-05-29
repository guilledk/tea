# TEA: Telos EVM Ansible

Setup/Manage Telos EVM nodes using this ansible playbook!

## quickstart

### config

All configuration is done though `config.yml`, some parameters to have in mind:

 - `node_name`: relevant to this specific node, example value `telos-mainnet-ansible`
 - `node_type`: chose one of three:
   - `local` - Local private chain with pre-seeded accounts and native+evm configuraton
   - `testnet` - Telos EVM Testnet node
   - `mainnet` - Telos EVM Mainnet node
 - `rpc.host` & `rpc.ws_host` - Set these to `0.0.0.0` if you want to server trafic from the outside world

By default `testnet` & `mainnet` nodes are read-only, set `rpc.signer_*` settings to be able to execute EVM transactions using the RPC endpoint.

### requires

 - `docker`
 - `ansible`
 - `python3`, `python3-requests`

### usage

    ansible-playbook playbooks/tea_start.yml --ask-become-pass
    ansible-playbook playbooks/tea_stop.yml --ask-become-pass

