# Makefile part of microcode_ctl package
#
# Copyright 2012 (c) Anton Arapov.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

PROGRAM         = intel-microcode2ucode
MICROCODE_INTEL = microcode-20151106.tgz

INS             = install
CC              = gcc
CFLAGS          = -g -Wall -O2 

DESTDIR         = 
PREFIX          = /usr/local

INSDIR          = $(PREFIX)/sbin
DOCDIR          = $(PREFIX)/share/doc/microcode_ctl
MICDIR          = /lib/firmware
MICDIRINTEL     = $(MICDIR)/intel-ucode

all: microcode_ctl

microcode_ctl: intel-microcode2ucode.c
	$(CC) $(CFLAGS) -o $(PROGRAM) intel-microcode2ucode.c
	tar -xOf $(MICROCODE_INTEL) | ./intel-microcode2ucode - >/dev/null

clean:
	rm -rf $(PROGRAM) intel-ucode

install:
	$(INS) -d $(DESTDIR)$(INSDIR) $(DESTDIR)$(DOCDIR) \
		$(DESTDIR)$(MICDIRINTEL)
	$(INS) -m 755 $(PROGRAM) $(DESTDIR)$(INSDIR)
	$(INS) -m 644 README $(DESTDIR)$(DOCDIR)
	$(INS) -m 644 intel-ucode/* $(DESTDIR)$(MICDIRINTEL)

uninstall:
	rm -rf $(DESTDIR)$(INSDIR)/$(PROGRAM) \
		$(DESTDIR)$(MICDIRINTEL) \
		$(DESTDIR)$(DOCDIR)

