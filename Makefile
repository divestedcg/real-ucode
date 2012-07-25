# Makefile part of microcode_ctl
#
# Copyright 2000 (c) Tigran Aivazian, Simon Trimmer.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.

PROGRAM		= microcode_ctl
MICROCODE	= intel-p6microcode-22June2000.txt
MANPAGE		= microcode_ctl.8
CC		= gcc
CFLAGS		= -g -Wall
INSDIR		= /usr/local/bin
MICDIR		= /etc
MANDIR		= /usr/local/man/man8
INS		= install

all: microcode_ctl

microcode_ctl:
	$(CC) $(CFLAGS) -o $(PROGRAM) microcode_ctl.c

clean:
	rm -f $(PROGRAM)

install:
	mkdir -p $(INSDIR)
	mkdir -p $(MANDIR)
	$(INS) -m 755 $(PROGRAM) $(INSDIR)
	$(INS) -m 644 $(MICROCODE) $(MICDIR)/microcode.dat
	$(INS) -m 644 $(MANPAGE) $(MANDIR)
	 
