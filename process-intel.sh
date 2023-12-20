#!/bin/sh
#License: CC0

umask 022;

iucode_tool --verbose --ignore-broken --overwrite --write-firmware=../microcode/intel-ucode/ Intel/*.bin;
