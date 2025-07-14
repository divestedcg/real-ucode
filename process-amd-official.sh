#!/bin/sh
#License: CC0

umask 022;

sh ../process-amd.sh

#move into place
rename ".bin" ".bin.official" *.bin
mv microcode_amd_fam*.bin.official ../microcode/amd-ucode/
