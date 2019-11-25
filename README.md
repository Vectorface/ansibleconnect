# Ansibleinviewer - Ansible Inventory Viewer 


Ansible Version | CI Status
---------|:---------
2.5    | [![Ansible 2.5 Build Status](https://travis-ci.com/psykulsk/ansibleinviewer.svg?branch=master&&env=USED_ANSIBLE_VERSION=2.5)](https://travis-ci.com/psykulsk/ansibleinviewer)
2.6    | [![Ansible 2.6 Build Status](https://travis-ci.com/psykulsk/ansibleinviewer.svg?branch=master&&env=USED_ANSIBLE_VERSION=2.6)](https://travis-ci.com/psykulsk/ansibleinviewer)
2.7    | [![Ansible 2.7 Build Status](https://travis-ci.com/psykulsk/ansibleinviewer.svg?branch=master&&env=USED_ANSIBLE_VERSION=2.7)](https://travis-ci.com/psykulsk/ansibleinviewer)
2.8    | [![Ansible 2.8 Build Status](https://travis-ci.com/psykulsk/ansibleinviewer.svg?branch=master&&env=USED_ANSIBLE_VERSION=2.8)](https://travis-ci.com/psykulsk/ansibleinviewer)
2.9    | [![Ansible 2.9 Build Status](https://travis-ci.com/psykulsk/ansibleinviewer.svg?branch=master&&env=USED_ANSIBLE_VERSION=2.9)](https://travis-ci.com/psykulsk/ansibleinviewer)



## SSH into all hosts in your inventory with one command.



Ansibleinviewer creates a bash script based on your ansible inventory.
That script will create a new tmux session and create a separate pane
for each one of your 'sshable' inventory hosts. Inside of each of the
panes an ssh connection to the pane's host will be established.

![](doc/demo.gif)

### Setup example (on Ubuntu):
```
sudo apt install tmux
sudo apt install sshpass
git clone https://github.com/psykulsk/ansibleinviewer.git
cd ansibleinviewer
python3 -m pip install .
```

### Usage examples:

Connect to all hosts in inventory:
```
source <(ansibleinviewer -i inventory.yml)
```

Connect to all hosts from group1 and group2:
```
source <(ansibleinviewer -i inventory.yml -g 'group1:group2')
```

Connect to all hosts from group1 except for hosts that are also in group2:
```
source <(ansibleinviewer -i inventory.yml -g 'group1:!group2')
```

Connect to all hosts from inventory except for hosts in group1:
```
source <(ansibleinviewer -i inventory.yml -g '!group1')
```

#### Possible flags

* `-i`, `--inventory` - Path to ansible inventory
* `-g`, `--groups` - Inventory groups of hosts to connect to (multiple groups should be concentrated with *:*. *!* in front of group name means that ansibleinviewer should not connect to hosts form this group)

### Authentication


#### ssh-agent

For authentication one can use ssh keys. `ansibleinviewer` will scan the inventory file for connection options (`ansible_ssh_common_args`, `ansible_ssh_user`, `ansible_host`). Ssh keys can be passed via them. Otherwise, one can use the `ssh-agent` tool. Environment args (`SSH_AGENT_PID` and `SSH_AUTH_SOCK`) will be passed to each one of the tmux shells.

##### ssh-agent setup example
```
eval $(ssh-agent)
ssh-add ~/.ssh/my_private_key\
```

#### sshpass

If `ansible_ssh_pass` variable is used in the inventory, one should installl the `sshpass` and make it discoverable via `PATH`. Please note that when using the sshpass, password will passed in plaintext and it will be saved in each of the tmux shells' history.
