# koji-scripts
This repo contains some random little things I have written over the past year for use with the Koji RPM build system.

Scripts
========
*copy_signed.py  - Silly little hack to copy signed RPMS into a separate dir on the system

*host_stat.py - Script I wrote for commnand line querying of builder status, does not require koji CLI client. Useful for NOC.

*MakeFile - This make file was designed to reside in the package directory within git, it allows you to quickly trigger scratch and full builds by issuing make scratch or make build after committing your package files to git.

Git-Hooks
=========
*pre-receive - This hook checks file extensions via commit logs, if it finds any binary archives it rejects the push.
