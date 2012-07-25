# Makefile part of microcode_ctl package
#
# Copyright 2012 (c) Anton Arapov.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

PROGRAM         = intel-microcode2ucode
MICROCODE_INTEL = microcode-20120606.tgz
MICROCODE_AMD   = amd-ucode-2012-01-17.tar

INS             = install
CC              = gcc
CFLAGS          = -g -Wall -O2 

DESTDIR         = 
PREFIX          = /usr/local

INSDIR          = $(PREFIX)/sbin
DOCDIR          = $(PREFIX)/share/doc/microcode_ctl
MICDIR          = /lib/firmware
MICDIRAMD       = $(MICDIR)/amd-ucode
MICDIRINTEL     = $(MICDIR)/intel-ucode

all: microcode_ctl

microcode_ctl: intel-microcode2ucode.c
	$(CC) $(CFLAGS) -o $(PROGRAM) intel-microcode2ucode.c
	tar -xOf $(MICROCODE_INTEL) | ./intel-microcode2ucode - >/dev/null
	mkdir amd-ucode && tar --strip-components 1 -xf $(MICROCODE_AMD) -C amd-ucode

clean:
	rm -rf $(PROGRAM) intel-ucode amd-ucode

install:
	$(INS) -d $(DESTDIR)$(INSDIR) $(DESTDIR)$(DOCDIR) \
		$(DESTDIR)$(MICDIRAMD) $(DESTDIR)$(MICDIRINTEL)
	$(INS) -m 755 $(PROGRAM) $(DESTDIR)$(INSDIR)
	$(INS) -m 644 README $(DESTDIR)$(DOCDIR)
	$(INS) -m 644 intel-ucode/* $(DESTDIR)$(MICDIRINTEL)
	$(INS) -m 644 amd-ucode/*.bin $(DESTDIR)$(MICDIRAMD)
	$(INS) -m 644 amd-ucode/*.bin.README $(DESTDIR)$(DOCDIR)
	$(INS) -m 644 amd-ucode/LICENSE $(DESTDIR)$(DOCDIR)/LICENSE.microcode_amd
	$(INS) -m 644 amd-ucode/README $(DESTDIR)$(DOCDIR)/README.microcode_amd
	$(INS) -m 644 amd-ucode/INSTALL $(DESTDIR)$(DOCDIR)/INSTALL.microcode_amd

uninstall:
	rm -rf $(DESTDIR)$(INSDIR)/$(PROGRAM) \
		$(DESTDIR)$(MICDIRINTEL) \
		$(DESTDIR)$(MICDIRAMD) \
		$(DESTDIR)$(DOCDIR)

