#!/usr/bin/env python3

from pathlib import Path

from leap.sugar import download_latest_snapshot, download_snapshot as _download_snapshot

from ansible.module_utils.basic import AnsibleModule

from tea.utils import stream_logs


def main():
    module_args = {
        'download_dir': {'type': 'str', 'required': True},
        'block_num': {'type': 'str', 'required': True},
        'network': {'type': 'str', 'required': True}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    try:
        block_num = int(module.params['block_num'])

    except ValueError:
        block_num = module.params['block_num']

    network: str = module.params['network']
    download_dir: Path = Path(module.params['download_dir']).resolve()
    download_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(block_num, int):
        snap_path = _download_snapshot(
            download_dir,
            block_num,
            progress=False,
            user_agent='TEA: Telos EVM Ansible'
        )
        block_num = int(snap_path.name.split('-')[-1].split('.')[0])

    elif block_num == 'latest':
        block_num, snap_path = download_latest_snapshot(
            download_dir,
            network='telos' if network == 'mainnet' else 'telostest',
            user_agent='TEA: Telos EVM Ansible'
        )

    else:
        raise ValueError('Wrong value for block_num param')

    module.exit_json(changed=True, result={
        'block_num': block_num,
        'snap_path': snap_path.name
    })


if __name__ == '__main__':
    main()
