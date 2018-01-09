# Makefile part of microcode_ctl package
#
# Copyright 2012 (c) Anton Arapov.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

MICROCODE_INTEL = microcode-20180108.tgz

INS             = install
CC              = gcc
CFLAGS          = -g -Wall -O2

DESTDIR         =
PREFIX          = /usr/local

DOCDIR          = $(PREFIX)/share/doc/microcode_ctl
MICDIR          = /lib/firmware
MICDIRINTEL     = $(MICDIR)/intel-ucode

all:
	tar -xf $(MICROCODE_INTEL) intel-ucode

clean:
	rm -rf intel-ucode

install:
	$(INS) -d $(DESTDIR)$(DOCDIR) \
		$(DESTDIR)$(MICDIRINTEL)
	$(INS) -m 644 README $(DESTDIR)$(DOCDIR)
	$(INS) -m 644 intel-ucode/* $(DESTDIR)$(MICDIRINTEL)

uninstall:
	rm -rf $(DESTDIR)$(MICDIRINTEL) \
		$(DESTDIR)$(DOCDIR)

