import pytest
import tempfile
import shutil
import os
import yaml
from ansible.cli.playbook import PlaybookCLI

@pytest.fixture
def ansible_playbook(request):
    node_type = request.param.get('template', 'local')
    user_config = request.param.get('config', {})

    temp_dir = Path(tempfile.mkdtemp())

    paths = [
        'library',
        'playbooks',
        'templates',
        'inventory.ini',
        'tea_up.yml'
        'tea_down.yml'
    ]

    for p in paths:
        source = Path() / p
        destination = temp_dir / p
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    with open(f'config.{node_type}.yml', 'r') as tpl_file:
        _config = yaml.load(tpl_file)

    _config.update(user_config)

    with open(temp_dir / 'config.yml', 'w') as file:
        yaml.dump(_config, file)

    # Prepare the CLI arguments
    cli_args = ['ansible-playbook', ]
    cli = PlaybookCLI(cli_args)
    cli.parse()
    
    # Run the playbook
    result = cli.run()
    
    # Yield the result and temporary directory
    yield result, temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)
