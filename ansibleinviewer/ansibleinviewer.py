#!/usr/bin/env python

import yaml
import argparse
import logging
from typing import Iterable, List

from ansibleinviewer.host import Host
from ansibleinviewer.inventoryparser import InventoryParser

logger = logging.getLogger(__name__)


def load_inventory_file(inventory_path: str) -> Iterable:
    with open(inventory_path) as inventory_file:
        inventory_data = yaml.safe_load(inventory_file)
    return inventory_data


def create_tmux_session_file(hosts: List[Host], vertical_panes):
    tmux_file_lines = [f"export PANE_WIDTH=$(expr $COLUMNS / {vertical_panes}) ; tmux new-session"]
    for index, host in enumerate(hosts):
        tmux_file_lines.append(f"send-keys '{host.connection_command}' C-m")
        if index == 0:
            tmux_file_lines.append(f"split-window -v")
        elif index != len(hosts) - 1:
            tmux_file_lines.append(f"select-pane -t {int(index / vertical_panes)}")
            tmux_file_lines.append(f"split-window -h")
    for index in range(len(hosts)):
        tmux_file_lines.append(f"resizep -t {index} -x $PANE_WIDTH")
    tmux_script = " \\; ".join(tmux_file_lines)
    print(tmux_script)


def parse_arguments():
    description = '''
    ansibleinviewer creates a shell command that sets up tmux layout and starts
    an ssh session for each "sshable" host from the inventory in a separate pane.
    Tmux available in PATH is required for this to work. 
    
    Example:
    source <(inviewer -i inventory.yml)
    '''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-i',
        '--inventory',
        required=True,
        help='Path to the ansible inventory file'
    )
    parser.add_argument(
        '-v',
        '--vertical_panes',
        default=2,
        type=int,
        help='Maximum number of tmux vertical panes'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    inventory_data = load_inventory_file(args.inventory)
    inventory_parser = InventoryParser(inventory_data)
    create_tmux_session_file(inventory_parser.get_hosts(), args.vertical_panes)


if __name__ == "__main__":
    main()
