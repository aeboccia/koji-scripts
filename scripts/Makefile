tag = <build-tag>
rev = HEAD
dir = $(shell pwd)
version = $(notdir $(dir))
package = $(notdir $(realpath ..))
koji = /bin/env koji
url = git+ssh://gituser@yourgit.server.fqdn/koji?

all: scratch

build:
	$(koji) build $(tag) '$(url)$(package)/$(version)/#$(rev)'

scratch:
	$(koji) build --scratch $(tag) '$(url)$(package)/$(version)/#$(rev)'

sources:
	spectool -g $(package).spec
