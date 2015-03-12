#!/usr/bin/python
#Author Anthony Boccia <anthony@boccia.me>
#This script will allow for quick determination of koji builders check in status via cli for users who do not have access to the Koji system i.e NOC
#It will output a message indicting all hosts up or that there may be issue, an exit value will also be returned. This makes it useable for nagios and other monitoring tools
#TODO: Add some brains outputting which host is not checking in
import koji
import time
import sys

def checkin(system_time,builder_time):
#This function will take each epoch timestamp and determine if it is larger than 60000, if it is more than 10 Minutes and 0 seconds has passed which means that the builder has not checked in within the desired timeframe
    dif = system_time - builder_time
    if dif > 60000:
        checkin = 1
    else:
        checkin = 0

    return checkin

def process_time(host_chktime):
#This function converts the timestamps to epoch to be further processed by the checkin function
    pattern = '%Y-%m-%d %H:%M:%S.%f'
    builder_time = int(time.mktime(time.strptime(host_chktime, pattern)))
    builder_time = int(round(float(builder_time)*100))
    #System_time will be equal to the time on the machine this script is executed from, ensure your system time is in sync with Koji's time
    system_time = int(round(float(time.time())*100))
    
    #Return time values
    return system_time,builder_time

#Main Logic, setup the session for Koji and begin looping through each host to verify their checkin times
session = koji.ClientSession('http://koji.example.org/kojihub')
hosts = session.listHosts()
#check_count will be used for keeping track of the returns from checkin function, if it is 0 in the end then all hosts have checked in, if it is > 0 then we have some hosts not checking in
check_count = 0
#Loop through all hosts and determine last checkin time for each
for host in hosts:
    if host['enabled'] is not False:
        host_id = host['id']
        host_chktime = session.getLastHostUpdate(host_id)
        
        #Call Functions
        system_time,builder_time = process_time(host_chktime)
        checkin = checkin(system_time,builder_time)
	check_count = check_count + checkin

if check_count > 0:
	print "One or more hosts are not checking in"
	sys.exit(2)
else:
	print "All are hosts checking in"
	sys.exit(0)
