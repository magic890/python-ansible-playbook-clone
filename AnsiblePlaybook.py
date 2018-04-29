import yaml
import subprocess
import sys


class AnsiblePlaybook:
    _playbook = []
    _hosts_dict = {}

    def __init__(self, hosts_path, playbook_path):
        self._hosts_dict = self._load_hosts(hosts_path)
        self._load_playbook(playbook_path)
        print 'Hosts dictionary:\n', self._hosts_dict

    def _load_playbook(self, playbook_path):
        with open(playbook_path, 'r') as stream:
            try:
                self._playbook = yaml.load(stream)
                print 'Playbook tree:\n', self._playbook
            except yaml.YAMLError as exc:
                print(exc)

    def _load_hosts(self, hosts_path):
        hosts = open(hosts_path, 'r')

        hosts_dict = {}
        current_host_group = {
            'to_add_to': False,
            'host_group': ''
        }

        for line in hosts:
            line_stripped = line.strip()

            # If it's a host group name
            if line_stripped.startswith('['):
                host_group_name = line_stripped[1:-1]
                hosts_dict[host_group_name] = list()

                current_host_group['to_add_to'] = True
                current_host_group['host_group'] = host_group_name

            # If it's a host name and we already have identified an host group name
            elif line_stripped and current_host_group['to_add_to']:
                if hosts_dict[current_host_group['host_group']] is None:
                    hosts_dict[current_host_group['host_group']] = [line_stripped]
                else:
                    hosts_dict[current_host_group['host_group']].append(line_stripped)

        return hosts_dict

    def run_tasks(self):
        # For every host group defined into Playbook
        for pb in self._playbook:

            # If the host group is defined also inside the hosts file
            if pb['hosts'] in self._hosts_dict:

                # For every task of that host group
                for task in pb['tasks']:

                    # In every server of the host group
                    for host in self._hosts_dict[pb['hosts']]:

                        # Run the task
                        print 'Running', task['name'], '( bash', task['bash'], ')', 'on', host, 'from group', pb['hosts']

                        # Configuration in ~/.ssh/config
                        ssh = subprocess.Popen(
                            ["ssh", "%s" % host, task['bash']],
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        result = ssh.stdout.readlines()
                        if not result:
                            error = ssh.stderr.readlines()
                            print >> sys.stderr, "ERROR: %s" % error
                        else:
                            print result


ap = AnsiblePlaybook('hosts', 'playbook.yml')
ap.run_tasks()
