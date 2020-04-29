from datetime import datetime
import re

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command



COMMANDS = [
    "traceroute mac 0001.6c4d.c0f7 0001.6c4d.c0f7",
    # "show ip int br",
    # "show ip arp",
    # "show platform resources",
]


def gather_commands(task, commands):
    for command in commands:
        output = task.run(netmiko_send_command, command_string=command)
        namesw = re.search(r'Destination\s[a-f0-9.]+\sfound on\s([\w-_]+)', output.result).group(1)
        port = re.search(rf'{namesw}\s.+=>\s([0-9FaGiTe/]+)', output).group(1)
        print(f"\nMac address found on switch {namesw} port {port}.\n")


def main():
    with InitNornir(config_file="nr-config-local.yaml") as nr:
        # lisbon = nr.filter(F(groups__contains="Lisbon"))
        nr.run(gather_commands, commands=COMMANDS)


if __name__ == '__main__':
    main()

