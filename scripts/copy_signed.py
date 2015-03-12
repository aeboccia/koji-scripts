#!/usr/bin/python
#Author Anthony Boccia <anthony@boccia.me>

#This script is to be used in conjunction with sign.py koji plugin, it will copy each signed rpm out of /mnt/koji/packages to the proper dest for mash to pick them up and mash together a repo
#Note this script requires that you have already configured sign.py koji plugin
#TODO 
#Verify each RPM is signed with a key matching the value of key_id - This should be done just before copy after the destination file existence check if statement
#Incorperate koji tag usage so each tag section from the config is read for the correct key_id just as is done with the sign.py plugin


import ConfigParser
import os
import glob
import shutil

#Get the KEYID out of the sign.conf
config_file = "/etc/koji-hub/plugins/sign.conf"
config = ConfigParser.ConfigParser()
config.read(config_file)
tag_name = "DEFAULT"
key_id = config.get(tag_name, 'key_id')
arch_list = ['x86_64', 'src']

#Check for dir structure for signed RPMS, create if necessary
path = "/mnt/koji/packages/"
packages = os.listdir (path)

#The first for loop ensures the copy process will occur for each architecture listed above
#The second for loop starts by looping through each package under the koji package dir
#Each time it loops it sets source variable to the full path where the rpms for the package can be found
#It then creates a list of each RPM in the x86_64 dir of the current package directory it is on in the loop
#The second for loop sets a source dest variable for each package in the list created in the previous step
#A check is done to ensure the destdir rpm does not already exist, this is to avoid unecessary file copy operations
#Finally the copy is executed
for arch in arch_list:
	for directory in glob.glob(os.path.join(path,'*/*/*')):
		source = directory + '/' + arch
		rpms_indir = os.listdir(source)
		for rpm_file in rpms_indir:	
			source = directory + '/' + arch + '/' + rpm_file
			dest = directory + '/data/signed/' + key_id + '/' + arch + '/' + rpm_file
			destdir = directory + '/data/signed/' + key_id + '/' + arch
			if os.path.isfile(dest):
				print "Signed RPM Already Exists", rpm_file
			else:
				if not os.path.exists(destdir):
					os.makedirs(destdir)
				shutil.copy2(source, destdir)
