# Ansible Playbook clone

Simple Ansible Playbook runner.

## Requirements

- Python 2.7
- PyYAML

## Usage

To run from the local folder, pointing to the `hosts` and `playbook.yml` contained here:

`$ python AnsiblePlaybook.py`

To customize the file location change the object creation, e.g: `ap = AnsiblePlaybook('/etc/ansible/hosts', 'playbook.yml')`
