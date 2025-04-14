#!/bin/sh
#License: CC0

umask 022;

#fam15h
./amd-ucodegen \
	AMD/cpu00600F00* \
	AMD/cpu00600F01* \
	AMD/cpu00600F10* \
	AMD/cpu00600F11* \
	AMD/cpu00600F12* \
	AMD/cpu00600F20* \
	AMD/cpu00610F00* \
	AMD/cpu00610F01* \
	AMD/cpu00630F00* \
	AMD/cpu00630F01* \
	AMD/cpu00660F00* \
	AMD/cpu00660F01* \
	AMD/cpu00670F00* \
	AMD/cpu00680F00* \
	AMD/cpu00680F01* \
	AMD/cpu00680F10* \
	AMD/cpu00690F00*

#fam16h
./amd-ucodegen \
	AMD/cpu00700F00* \
	AMD/cpu00700F01* \
	AMD/cpu00730F00* \
	AMD/cpu00730F01*

#fam17h
./amd-ucodegen \
	AMD/cpu00800F00* \
	AMD/cpu00800F10* \
	AMD/cpu00800F11* \
	AMD/cpu00800F12* \
	AMD/cpu00800F82* \
	AMD/cpu00810F00* \
	AMD/cpu00810F10* \
	AMD/cpu00810F11* \
	AMD/cpu00810F80* \
	AMD/cpu00810F81* \
	AMD/cpu00820F00* \
	AMD/cpu00820F01* \
	AMD/cpu00830F00* \
	AMD/cpu00830F10* \
	AMD/cpu00850F00* \
	AMD/cpu00860F00* \
	AMD/cpu00860F01* \
	AMD/cpu00860F81* \
	AMD/cpu00870F00* \
	AMD/cpu00870F10* \
	AMD/cpu00880F40* \
	AMD/cpu00890F00* \
	AMD/cpu00890F01* \
	AMD/cpu00890F02* \
	AMD/cpu00890F10* \
	AMD/cpu008A0F00*

#fam19h
./amd-ucodegen \
	AMD/cpu00A00F00* \
	AMD/cpu00A00F10* \
	AMD/cpu00A00F11* \
	AMD/cpu00A00F12* \
	AMD/cpu00A00F80* \
	AMD/cpu00A00F82* \
	AMD/cpu00A10F00* \
	AMD/cpu00A10F01* \
	AMD/cpu00A10F0B* \
	AMD/cpu00A10F10* \
	AMD/cpu00A10F11* \
	AMD/cpu00A10F12* \
	AMD/cpu00A10F80* \
	AMD/cpu00A10F81* \
	AMD/cpu00A20F00* \
	AMD/cpu00A20F10* \
	AMD/cpu00A20F12* \
	AMD/cpu00A40F00* \
	AMD/cpu00A40F40* \
	AMD/cpu00A40F41* \
	AMD/cpu00A50F00* \
	AMD/cpu00A60F00* \
	AMD/cpu00A60F11* \
	AMD/cpu00A60F12* \
	AMD/cpu00A70F00* \
	AMD/cpu00A70F40* \
	AMD/cpu00A70F41* \
	AMD/cpu00A70F42* \
	AMD/cpu00A70F52* \
	AMD/cpu00A70F80* \
	AMD/cpu00A70FC0* \
	AMD/cpu00A80F00* \
	AMD/cpu00A80F01* \
	AMD/cpu00A90F00* \
	AMD/cpu00A90F01* \
	AMD/cpu00AA0F00* \
	AMD/cpu00AA0F01* \
	AMD/cpu00AA0F02*

#fam1ah
./amd-ucodegen \
	AMD/cpu00B00F00* \
	AMD/cpu00B00F10* \
	AMD/cpu00B00F20* \
	AMD/cpu00B00F21* \
	AMD/cpu00B10F00* \
	AMD/cpu00B10F10* \
	AMD/cpu00B20F40* \
	AMD/cpu00B40F00* \
	AMD/cpu00B40F40* \
	AMD/cpu00B60F00* \
	AMD/cpu00B70F00*

#move into place
mv microcode_amd_fam*.bin ../microcode/amd-ucode/
