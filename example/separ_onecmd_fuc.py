#! /usr/bin/env python

# Import libraries
from netmiko import ConnectHandler
import re

from example.device_info import nxos1 as device  # noqa


# Create a CLI command template
show_ver_config_temp = "show version"
show_diag_shass_temp = "show diag chassis eeprom"
sho_mac_tabl = "show mac add"

# Open CLI connection to device
connection = ConnectHandler(ip=device["address"],
                    port=device["ssh_port"],
                    username=device["username"],
                    device_type=device["device_type"],
                    password=device["password"])


# Create desired CLI command and send to device
version = connection.send_command(show_ver_config_temp)
diag = connection.send_command(show_diag_shass_temp)

print(version)
print(diag)
# Send configuration to device
#
# try:
#     # Use regular expressions to parse the output for desired data
#     imagename = re.search(r'Cisco IOS.+\(([A-Z0-9_-]*)\)', version).group(1)
#     imagever = re.search(r'Version\s([A-Za-z0-9\._-]*)', version).group(1)
#     hostname = re.search(r'(.+)\suptime\sis', version).group(1)
#     modelname = re.search(r'\(PID\)\s:\s([A-Z0-9]+)', diag).group(1)
#
#
#     # Print the info to the screen
#     # ms-gw-01|ISR4451/K9|BLD_V154_3_S_XE313_THROTTLE_LATEST |PE |CDP is ON,5 peers|Clock in Sync
#     print(f"\n{hostname}|{modelname}|{imagever}\n")
#
# except Exception:
#     print("Regexp not work.")