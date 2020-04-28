#! /usr/bin/env python

# Import libraries
from netmiko import ConnectHandler
import re

from example.device_info import ios_xe1 as device  # noqa


# Create a CLI command template
show_ver_config_temp = "show version"
show_diag_shass_temp = "show diag chassis eeprom"
show_cdp = "show cdp neighbors"
show_ntp = "show ntp status"
test_ntp = "ping 192.168.1.1"
conf_ntp = "ntp server 192.168.1.1"

# Open CLI connection to device
connection = ConnectHandler(ip=device["address"],
                    port=device["ssh_port"],
                    username=device["username"],
                    password=device["password"],
                    device_type=device["device_type"])


# Create desired CLI command and send to device
version = connection.send_command(show_ver_config_temp)
diag = connection.send_command(show_diag_shass_temp)
cdpstatus = connection.send_command(show_cdp)
ntpstatus = connection.send_command(show_ntp)

# Send configuration to device
if "%NTP is not enabled." in ntpstatus:
    ntptest = re.search(r'Success rate is ([0-9]+) percent', connection.send_command(test_ntp)).group(1)
    if "0" in ntptest:
        confntp = connection.send_config_set(conf_ntp)
        print(confntp)
        ntpstatus = connection.send_command(show_ntp)
        ntp = re.search(r'Clock is\s([a-z]+),', ntpstatus).group(1)
    else:
        ntp = "NTP server not reachable"
else:
    ntp = re.search(r'Clock is\s([a-z]+),', ntpstatus).group(1)

try:
    # Use regular expressions to parse the output for desired data
    imagename = re.search(r'Cisco IOS.+\(([A-Z0-9_-]*)\)', version).group(1)
    imagever = re.search(r'Version\s([A-Za-z0-9\._-]*)', version).group(1)
    hostname = re.search(r'(.+)\suptime\sis', version).group(1)
    modelname = re.search(r'\(PID\)\s:\s([A-Z0-9]+)', diag).group(1)

    if "NPE" in imagename:
        npeimage = "NPE"
    else:
        npeimage = "PE"

    if "% CDP is not enabled" in cdpstatus:
        cdp = "CDP is OFF"
        cdppeers = "0"
    else:
        cdp = "CDP is ON"
        cdppeers = re.search(r'\s:\s([0-9]+)', cdpstatus).group(1)

    # Print the info to the screen
    # ms-gw-01|ISR4451/K9|BLD_V154_3_S_XE313_THROTTLE_LATEST |PE |CDP is ON,5 peers|Clock in Sync
    print(f"\n{hostname}|{modelname}|{imagever}|{npeimage}|{cdp}, {cdppeers} peers|{ntp}\n")

except Exception:
    print("Regexp not work.")