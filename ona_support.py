jeff@ona-8295e4:/$ cat support.py
#!/usr/bin/env python
#Stealthwatch Cloud Sensor Support Script
#Author: Jeff Moncrief, 3/2019
import subprocess
import os

#Operating System & Distribution Info
def uname_func():

    uname = "uname"
    uname_arg = "-a"
    print "*** Gathering system information with %s command:\n" % uname
    subprocess.call([uname, uname_arg])

#Disk Information
def disk_func():

    diskspace = "df"
    diskspace_arg = "-h"
    print "*** Gathering diskspace information %s command:\n" % diskspace
    subprocess.call([diskspace, diskspace_arg])

#Cloud Connectivity Test
def connection_func():

    http_command = "curl"
    http_arg = "https://sensor.ext.obsrvbl.com"
    print "*** Gathering cloud connectivity information %s command:\n" % http_command
    subprocess.call([http_command, http_arg])

#IPTables Output
def iptables_func():

    iptables = "iptables"
    iptables_arg = "-L"
    print "*** Gathering IPTables output with %s command:\n" % iptables
    subprocess.call([iptables, iptables_arg])

#Config.local Output
def config_func():

    config = "cat"
    config_arg = "/opt/obsrvbl-ona/config.local"
    print "*** Gathering config.local config with %s command:\n, BLANK is OK" % config
    subprocess.call([config, config_arg])

#ONA Pusher File Log
def pusher_func():

    pusher = "tail"
    pusher_arg = "/opt/obsrvbl-ona/logs/ona_service/ona-pna-pusher.log"
    print "*** Gathering ONA Pusher log with %s command:\n" % pusher
    subprocess.call([pusher, pusher_arg])

#Packet Capture Command

print "*** Performing TCPDump"
os.popen("sudo -S tcpdump -w capture.pcap -c 10 udp", 'w').write("mypassword")

#Main Function to Call All Functions
def main():
    uname_func()
    disk_func()
    connection_func()
    iptables_func()
    config_func()
    pusher_func()

main()
jeff@ona-8295e4:/$
