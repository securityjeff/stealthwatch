#!/usr/bin/env python
#Test Plan Brute Force Script
#Author: Jeff Moncrief, 5/2020

import os
import time 


count = 0
while (count < 1000):
   print "*****  PERFORMING SCAN NUMBER: ", count 
   os.system("nmap -Pn -p 3389 <your exposed workload ip address>")
   time.sleep(15)
   count = count + 1

print "Good bye!"
