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
    f = open("support.txt", "w")
    subprocess.call([uname, uname_arg], stdout=f)

#Disk Information
def disk_func():

    diskspace = "df"
    diskspace_arg = "-h"
    print "*** Gathering diskspace information %s command:\n" % diskspace
    f = open("support.txt", "a+")
    subprocess.call([diskspace, diskspace_arg], stdout=f)

#Cloud Connectivity Test
def connection_func():

    http_command = "curl"
    http_arg = "https://sensor.ext.obsrvbl.com"
    print "*** Gathering cloud connectivity information %s command:\n" % http_command
    f = open("support.txt", "a+")
    subprocess.call([http_command, http_arg], stdout=f)

#IPTables Output
def iptables_func():

    iptables = "iptables"
    iptables_arg = "-L"
    print "*** Gathering IPTables output with %s command:\n" % iptables
    f = open("support.txt", "a+")
    subprocess.call([iptables, iptables_arg], stdout=f)

#Config.local Output
def config_func():

    config = "cat"
    config_arg = "/opt/obsrvbl-ona/config.local"
    print "*** Gathering config.local config with %s command:\n, BLANK is OK" % config
    f = open("support.txt", "a+")
    subprocess.call([config, config_arg], stdout=f)

#ONA Pusher File Log
def pusher_func():

    pusher = "tail"
    pusher_arg = "/opt/obsrvbl-ona/logs/ona_service/ona-pna-pusher.log"
    print "*** Gathering ONA Pusher log with %s command:\n" % pusher
    f = open("support.txt", "a+")
    subprocess.call([pusher, pusher_arg], stdout=f)

#Packet Capture Command

print "*** Performing TCPDump"
os.popen("sudo -S tcpdump -w capture.pcap -c 1000 udp", 'w').write("mypassword")

#TAR files into Support bundle files
def bundle_func():

    os.system("tar cvf bundle.tar support.txt capture.pcap")


#Main Function to Call All Functions
def main():
    uname_func()
    disk_func()
    connection_func()
    iptables_func()
    config_func()
    pusher_func()
    bundle_func()

main()
