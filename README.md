real-ucode
==========

Overview
--------
- AMD appears to primarily only include microcode for enterprise platforms in the linux-firmware repo.
  - https://divested.dev/misc/amd-ucode.txt
- Intel also appears to miss a few and also doesn't always include the latest available.
  - https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/issues/10

Compatibility
-------------
- CentOS 9/Stream
- Fedora 38/39

License
-------
- See the LICENSE file

Prebuilts
---------
- Fedora via Divested-RPM: https://divested.dev/index.php?page=software#divested-release

Usage
-----
- Install the package
- Run the actual installer (necessary to prevent package conflict with linux-firmware): sudo install-real-ucode

Verifying it took
-----------------
- You can do this a few ways:
  - Running `lscpu` before and after, then diffing
  - Checking logs, eg. `journalctl -b0 | grep -i microcode` then `-b-1`

Status
------
| Board | CPU | Version | Status |
| ----- | --- | ------- | ------ |
| ASUS M1605YA | 7530U | 302 | 0x0a50000d -> 0x0a50000f |
| ASUS M5402RA | 6800H | 301 | severe breakage, stuck at 400MHz, can't suspend |
| ASUS TUF Gaming X670E | 7950X | 1809 | already latest |
| Gigabyte B450-DS3H | 3600 | F65b | already latest |
| Lenovo S340-15API | 3500U | amcn31ww | already latest |
| MSI A5M-288 | 5700U | E155LAMS.115 | 0x08608103 -> 0x08608104 |
| MSI X570 A-PRO | 5900X | 7C37vHL | 0x0a20120a -> 0x0a20120e |
| ? | 5800H | ? | 0xa50000c -> 0xa50000f |

Building
--------
- git clone [THIS REPO]
- CentOS: rpmbuild -ba brace.spec
- Fedora: rpmbuild -ba brace.spec

Updating the microcode
----------------------
- git clone [THIS REPO]
- git clone https://github.com/platomav/CPUMicrocodes
- git clone https://github.com/AndyLavr/amd-ucodegen
- cd amd-ucodegen
- git apply ../amd-ucodegen-tweak.diff
- make
- cd ../CPUMicrocodes
- mv ../amd-ucodegen/amd-ucodegen .
- source ../process-amd.sh
- source ../process-intel.sh
- update version/date in real-ucode.sh
- commit it with the short git hash of the CPUMicrocodes repo

Credits
-------
- Huge thanks to Plato Mavropoulos for the actual microcode collection
	- https://github.com/platomav/CPUMicrocodes
- Andy Lavr for the AMD conversion program
	- GPL-2.0: https://github.com/AndyLavr/amd-ucodegen

Other Notes
-----------
- There is an Arch Linux port on the AUR by @moparisthebest:
  - https://aur.archlinux.org/packages/amd-real-ucode-git
  - https://aur.archlinux.org/packages/intel-real-ucode-git
