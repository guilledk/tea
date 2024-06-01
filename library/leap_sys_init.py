#!/usr/bin/env python3

import time

from pathlib import Path

import requests

from leap.cleos import CLEOS

from ansible.module_utils.basic import AnsibleModule

from tea.utils import stream_logs
from tea.cleos_evm import CLEOSEVM


def main():
    module_args = {
        'playbook_vars': {'type': 'dict', 'required': True}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    playbook_vars = module.params['playbook_vars']

    node_type: str = playbook_vars.get('node_type')
    chain_id: str = playbook_vars.get('leap').get('chain_id')
    chain_id_evm: int = int(playbook_vars.get('translator').get('chain_id'))
    cleos_url: str = playbook_vars.get('leap_http_endpoint')
    cleos_evm_url: str = playbook_vars.get('rpc_endpoint')
    log_path: Path = Path(playbook_vars.get('leap_log_file'))
    translator_start_block: int = int(playbook_vars.get('translator_start_block'))
    skip_init: bool = playbook_vars.get('leap').get('skip_init', False)
    evm_contract: str | None = playbook_vars.get('leap').get('evm_contract', None)
    sig_provider: str | None = playbook_vars.get('leap').get('ini').get('sig_provider', None)
    contracts_dir: Path = Path('./templates/leap/contracts').resolve()

    cleos = CLEOSEVM(
        cleos_url,
        evm_url=cleos_evm_url,
        chain_id=chain_id_evm
    )

    if isinstance(sig_provider, str):
        producer_key = sig_provider.split('=KEY:')[-1]
        cleos.import_key('eosio', producer_key)

    cleos.load_abi_file('eosio', f'{contracts_dir}/eosio.system/eosio.system.abi')
    cleos.load_abi_file('eosio.evm', f'{contracts_dir}/eosio.evm/regular/regular.abi')
    cleos.load_abi_file('eosio.token', f'{contracts_dir}/eosio.token/eosio.token.abi')

    if not skip_init:
        output = ''
        for msg in stream_logs(log_path, lines=400, timeout=60*10):
            output += msg
            if 'Produced' in msg:
                break

        # await for nodeos to produce a block
        cleos.wait_blocks(4)

        is_fresh = (
            'No existing chain state or fork database. '
            'Initializing fresh blockchain state and resetting fork database.' in output
        )

        if is_fresh:
            cleos.boot_sequence(
                contracts=contracts_dir, remote_node=CLEOS('https://testnet.telos.net'))

            cleos.deploy_evm(contracts_dir / evm_contract)

        # wait until nodeos apis are up
        started = False
        for i in range(60):
            try:
                nodeos_init_info = cleos.get_info()
                current_chain_id = nodeos_init_info['chain_id']

                if chain_id != current_chain_id:
                    raise ValueError(
                        f'chain id returned ({current_chain_id}) '
                        f'from nodeos differs from one on config ({chain_id})')

                started = True
                break

            except requests.exceptions.ConnectionError:
                print('connection error trying to get chain info...')
                time.sleep(1)

        if not started:
            raise AssertionError('Nodeos APIs failed to be up!')

        print(
            'nodeos has started, waiting until blocks.log '
            f'contains block number {translator_start_block}'
        )
        cleos.wait_block(
            translator_start_block - 1, progress=True, interval=5)

        # create funded evm account
        if (node_type == 'local' and
            is_fresh and
            not skip_init):
            cleos.create_test_evm_account()

    module.exit_json(result={})


if __name__ == '__main__':
    main()
