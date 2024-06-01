#!/usr/bin/env python3

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule

from tea.utils import stream_logs


def main():
    module_args = {
        'playbook_vars': {'type': 'dict', 'required': True}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    playbook_vars = module.params['playbook_vars']

    log_path: Path = Path(playbook_vars.get('leap_log_file'))

    # skip wait if --replay-blockchain  in additional_nodeos_params
    # or if peer list len == 0
    for msg in stream_logs(log_path, timeout=60*10):
        if 'Received' in msg:
            break

    module.exit_json(result={})


if __name__ == '__main__':
    main()
