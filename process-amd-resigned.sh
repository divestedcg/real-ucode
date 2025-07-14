#!/bin/sh
#License: CC0

umask 022;

for ucode in AMD/cpu*
do
	../compiled/zentool resign $ucode;
done

sh ../process-amd.sh

#move into place
rename ".bin" ".bin.resigned" *.bin
mv microcode_amd_fam*.bin.resigned ../microcode/amd-ucode/
