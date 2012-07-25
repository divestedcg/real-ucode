# Makefile part of microcode_ctl package
#
# Copyright 2000 (c) Simon Trimmer, Tigran Aivazian.
# Copyright 2012 (c) Anton Arapov.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

PROGRAM			= microcode_ctl
MANPAGE			= microcode_ctl.8
MICROCODE_INTEL	= microcode-20120606.tgz
MICROCODE_AMD	= amd-ucode-2012-01-17.tar

INS				= install
CC				= gcc
KERNELHEADER 	= /usr/src/linux/include
CFLAGS			= -g -Wall -O2 -I $(KERNELHEADER)

DESTDIR			=
PREFIX			= /usr/local

INSDIR			= $(PREFIX)/sbin
MANDIR			= $(PREFIX)/share/man/man8
DOCDIR			= $(PREFIX)/share/doc/microcode_ctl
MICDIR			= /lib/firmware

UDEVRULES		= microcode_ctl.rules
UDEVRULESTO		= /lib/udev/rules.d

all: microcode_ctl

microcode_ctl: microcode_ctl.c
	$(CC) $(CFLAGS) -o $(PROGRAM) microcode_ctl.c
	mkdir intel-ucode amd-ucode
	tar xfz $(MICROCODE_INTEL) -C intel-ucode
	tar --strip-components 1 -xf $(MICROCODE_AMD) -C amd-ucode

clean:
	rm -rf $(PROGRAM) intel-ucode amd-ucode

install:
	$(INS) -d $(DESTDIR)$(INSDIR) $(DESTDIR)$(MICDIR)/amd-ucode \
		$(DESTDIR)$(MANDIR) $(DESTDIR)$(UDEVRULESTO) $(DESTDIR)$(DOCDIR)
	$(INS) -m 755 $(PROGRAM) $(DESTDIR)$(INSDIR)
	$(INS) -m 644 $(MANPAGE) $(DESTDIR)$(MANDIR)
	gzip -9f $(DESTDIR)$(MANDIR)/$(MANPAGE)
	$(INS) -m 644 $(UDEVRULES) $(DESTDIR)$(UDEVRULESTO)/$(UDEVRULES)
	$(INS) -m 644 intel-ucode/microcode.dat $(DESTDIR)$(MICDIR)
	$(INS) -m 644 amd-ucode/microcode_amd.bin $(DESTDIR)$(MICDIR)/amd-ucode/
	$(INS) -m 644 amd-ucode/microcode_amd_fam15h.bin $(DESTDIR)$(MICDIR)/amd-ucode/
	$(INS) -m 644 amd-ucode/microcode_amd.bin.README \
		$(DESTDIR)$(DOCDIR)/README.microcode_amd.bin
	$(INS) -m 644 amd-ucode/microcode_amd_fam15h.bin.README \
		$(DESTDIR)$(DOCDIR)/README.microcode_amd_fam15h.bin
	$(INS) -m 644 amd-ucode/LICENSE $(DESTDIR)$(DOCDIR)/LICENSE.microcode_amd
	$(INS) -m 644 amd-ucode/README $(DESTDIR)$(DOCDIR)/README.microcode_amd
	$(INS) -m 644 amd-ucode/INSTALL $(DESTDIR)$(DOCDIR)/INSTALL.microcode_amd

device:
	mkdir -p $(DESTDIR)/dev/cpu
	mknod $(DESTDIR)/dev/cpu/microcode c 10 184

uninstall:
# shame there isn't reverse of install...
	rm -rf $(DESTDIR)$(INSDIR)/$(PROGRAM) \
		$(DESTDIR)$(MANDIR)/$(MANPAGE).gz \
		$(DESTDIR)$(UDEVRULESTO)/$(UDEVRULES) \
		$(DESTDIR)$(MICDIR)/amd-ucode \
		$(DESTDIR)$(MICDIR)/microcode.dat \
		$(DESTDIR)$(DOCDIR)

