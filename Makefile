# Makefile part of microcode_ctl
#
# Copyright 2000 (c) Simon Trimmer, Tigran Aivazian.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

PROGRAM		= microcode_ctl
MICROCODE	= intel-p6microcode-22June2000.txt
MANPAGE		= microcode_ctl.8
RCFILE		= microcode_ctl.start

INS		= install
CC		= gcc
KERNELHEADER    = /usr/src/linux/include
CFLAGS		= -g -Wall -O2 -I $(KERNELHEADER)

DESTDIR		=
PREFIX		= /usr/local

INSDIR		= $(PREFIX)/sbin
MANDIR		= $(PREFIX)/man/man8
DOCDIR		= $(PREFIX)/doc
MICDIR		= /etc

RCDIR		= /etc/rc.d
RCHOMEDIR	= init.d
RCLINKDIR	= rc3.d
RCLINKNAME	= S95microcode_ctl

RCFILETO	= $(RCDIR)/$(RCHOMEDIR)
RCLINKTO	= $(RCDIR)/$(RCLINKDIR)

all: microcode_ctl

microcode_ctl: microcode_ctl.c
	$(CC) $(CFLAGS) -o $(PROGRAM) microcode_ctl.c

clean:
	rm -f $(PROGRAM)

install:
	$(INS) -d	$(DESTDIR)$(INSDIR) $(DESTDIR)$(MICDIR) \
			$(DESTDIR)$(MANDIR) $(DESTDIR)$(RCFILETO) \
			$(DESTDIR)$(RCLINKTO)
			

	$(INS) -s -m 755 $(PROGRAM) $(DESTDIR)$(INSDIR)
	$(INS) -m 644 $(MICROCODE) $(DESTDIR)$(MICDIR)/microcode.dat

	$(INS) -m 644 $(MANPAGE) $(DESTDIR)$(MANDIR)
	gzip -9f $(DESTDIR)$(MANDIR)/$(MANPAGE)

	$(INS) -m 755 $(RCFILE) $(DESTDIR)$(RCFILETO)/$(RCFILE)

	ln -fs ../$(RCHOMEDIR)/$(RCFILE) $(DESTDIR)/$(RCLINKTO)/$(RCLINKNAME)

device:
	mkdir -p $(DESTDIR)/dev/cpu
	mknod $(DESTDIR)/dev/cpu/microcode c 10 184

