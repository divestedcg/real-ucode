# Makefile part of microcode_ctl package
#
# Copyright 2000 (c) Simon Trimmer, Tigran Aivazian.
# Copyright 2012 (c) Anton Arapov.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

PROGRAM		= microcode_ctl
MANPAGE		= microcode_ctl.8

INS			= install
CC			= gcc
KERNELHEADER = /usr/src/linux/include
CFLAGS		= -g -Wall -O2 -I $(KERNELHEADER)

DESTDIR		=
PREFIX		= /usr/local

INSDIR		= $(PREFIX)/sbin
MANDIR		= $(PREFIX)/share/man/man8
MICDIR		= /lib/firmware

RCFILE		= microcode_ctl.start
RCFILEFINAL	= microcode_ctl
# this is a bit nasty...
RCDIR		= $(shell if [ -d /etc/init.d ]; then echo "/etc"; else echo "/etc/rc.d"; fi)
RCHOMEDIR	= init.d
RCFILETO	= $(RCDIR)/$(RCHOMEDIR)

all: microcode_ctl

microcode_ctl: microcode_ctl.c
	$(CC) $(CFLAGS) -o $(PROGRAM) microcode_ctl.c
	echo "$(RCDIR)/$(RCHOMEDIR)/microcode_ctl" > microcode-filelist

clean:
	rm -f $(PROGRAM)

install:
	$(INS) -d	$(DESTDIR)$(INSDIR) $(DESTDIR)$(MICDIR) \
			$(DESTDIR)$(MANDIR) $(DESTDIR)$(RCFILETO) \
			$(DESTDIR)$(RCLINKTO)

	$(INS) -m 755 $(PROGRAM) $(DESTDIR)$(INSDIR)

	$(INS) -m 644 $(MANPAGE) $(DESTDIR)$(MANDIR)
	gzip -9f $(DESTDIR)$(MANDIR)/$(MANPAGE)

	$(INS) -m 755 $(RCFILE) $(DESTDIR)$(RCFILETO)/$(RCFILEFINAL)

ifndef DESTDIR
		chkconfig --add $(RCFILEFINAL)
else
		echo "MAKE: Skipping chkconfig operation (rpm build?)"
endif

device:
	mkdir -p $(DESTDIR)/dev/cpu
	mknod $(DESTDIR)/dev/cpu/microcode c 10 184

uninstall:
ifndef DESTDIR
	chkconfig --del $(RCFILEFINAL)
endif
# shame there isn't reverse of install...
	rm $(DESTDIR)$(INSDIR)/$(PROGRAM) \
		$(DESTDIR)$(MANDIR)/$(MANPAGE).gz \
		$(DESTDIR)$(RCFILETO)/$(RCFILEFINAL)
