real-ucode
==========

Background
----------
- AMD and Intel both are actively harming users by providing incomplete and delayed microcode updates (to Linux)
- Why microcode?
  - Microcode updates provide functional and security fixes and are most importantly available out-of-band. This allows operating systems to provide rapid updates side stepping the need for vendor BIOS/EFI update releases and their installation.

Market Segmentation
-------------------
This is most clear with AMD by the following two reasons. Their goal is to push cloud providers to enterprise platforms and discourage use of cheaper consumer platforms.

- AMD only provides direct microcode updates for enterprise platforms. Consumer platforms only get microcode updates via AGESA updates.
  - Direct microcode updates are hot-loadable offering minimal downtime.
  - AGESA updates would require eg. the shuffling of virtual machines to another system and a reboot of the host.
- AMD actively delays updates to consumer systems by 2-3 months
  - This is before the delay from vendors providing system/motherboard updates

| bulletin | publication date | earliest enterprise microcode | earliest consumer agesa |
| -------- | ---------------- | ---------------------------- | ----------------------- |
| [AMD-SB-7005](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7005.html) | 2023-08-08 | 2023-06-09 | 2023-08-22 |
| [AMD-SB-7008](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7008.html) | 2023-07-24 | 2023-06-06 | 2023-11-21 |
| [AMD-SB-7014](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7014.html) | 2024-08-09 | 2024-05-03 | 2024-07-30 |

Stats (2025-03-09)
------------------
| provider | # supported cpuids | # outdated |
| -------- | ------------------ | ---------- |
| [Intel (official)](https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/) | 275 | 41 |
| Intel (real-ucode) | 616 | 2 |
| [AMD (linux-firmware)](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amd-ucode) | 41 | 23 |
| AMD (real-ucode) | 107 | 3 |

Compatibility
-------------
- CentOS 9/Stream
- Fedora 38/39/40/41/etc.

License
-------
- See the LICENSE file

Prebuilts
---------
- Fedora via Divested-RPM: https://divested.dev/index.php?page=software#divested-release

Special AMD Incompatibility Notice (2025-03-02)
-----------------------------------------------
- After the recent AMD microcode signature verification vulnerability (CVE-2024-56161), microcode dated after 2024-11 will fail to load on pre 2025-01 bioses
- You can install an older version from our repository by: `sudo dnf install amd-ucode-firmware-20250224-1`
- Then disable updates for it: edit /etc/dnf/dnf.conf and append `excludepkgs=amd-ucode-firmware`
- You may also need an extra kernel command line argument since the Linux kernel has a hardcoded list of select ucode hashes: `sudo grubby --update-kernel=ALL --args="microcode.amd_sha_check=off"`
   - Test first without it
   - This evidently taints the kernel
- Closely watch your vendor for new bios updates

Usage
-----
- Once Divested-RPM is installed, simply running `dnf update` will pull in our `amd-ucode-firmware` and `microcode_ctl` packages due to their higher epoch version
- Alternatively build them yourself and install them manually
- Regenerate initramfs: `dracut -f`
- Reboot

Verifying it took
-----------------
- You can do this a few ways:
  - Checking logs, eg. `journalctl -b0 | grep -i microcode` then `-b-1`
  - Less reliable, running `lscpu` before and after, then diffing

Status (outdated)
-----------------
| Board | CPU | CPUID | Version | Change | Notes |
| ----- | --- | ----- | ------- | ------ | ----- |
| ASUS M1605YA | 7530U | 00A50F00 | 302 | 0x0a50000d -> 0x0a50000f |
| ASUS M5402RA | 6800H | 00A40F41 | 301 | 0x0a404101 -> 0x0a404102 | severe breakage, stuck at 400MHz after suspend |
| ASUS TUF Gaming X570 | 5900X | 00A20F10 | 5003 | already latest |
| ASUS TUF Gaming X670E | 7950X | 00A60F12 | 1809 | already latest |
| Gigabyte B450-DS3H | 3600 | 00870F10 | F65b | already latest |
| Lenovo 15ACH6A | 5800H | 00A50F00 | G9CN33WW | 0x0a50000c -> 0x0a50000f |
| Lenovo S340-15API | 3500U | 00810F81 | AMCN31WW | already latest |
| MSI A5EFK | 5800H | 00A50F00 | E15CKAMS.10C | 0x0a50000? -> 0x0a50000f |
| MSI A5M-288 | 5700U | 00860F81 | E155LAMS.115 | 0x08608103 -> 0x08608104 |
| MSI X570 A-PRO | 5900X | 00A20F12 | 7C37vHL | 0x0a20120a -> 0x0a20120e |

Building
--------
- git clone [THIS REPO]
- CentOS: rpmbuild -ba real-ucode.spec
- Fedora: rpmbuild -ba real-ucode.spec

Maintaining this repo
---------------------
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
- update version/date in real-ucode.spec
- commit it with the short git hash of the CPUMicrocodes repo

Credits
-------
- Huge thanks to Plato Mavropoulos for the actual microcode collection
	- https://github.com/platomav/CPUMicrocodes
- Guenter Roeck for the AMD conversion program
	- GPL-2.0: https://github.com/AndyLavr/amd-ucodegen
- @chinobino for their extensive microcode collection
	- https://winraid.level1techs.com/t/offer-intel-amd-via-cpu-microcode-archives-1995-present/102857
- Contributors to the Winraid/Level1Techs forum, such as @westlake, @lfb6, and @jen11, for additional microcode
	- https://winraid.level1techs.com/t/intel-amd-via-freescale-cpu-microcode-repositories-discussion/32301

Other Notes
-----------
- There is an Arch Linux port on the AUR by @moparisthebest:
  - https://aur.archlinux.org/packages/amd-real-ucode-git
  - https://aur.archlinux.org/packages/intel-real-ucode-git
- There is a similar project for NixOS here: https://github.com/e-tho/ucodenix
- Forum threads for this are here:
  - https://winraid.level1techs.com/t/real-ucode-all-the-microcodes-but-packaged/103179
  - https://discuss.privacyguides.net/t/real-ucode-a-fedora-package-with-all-the-microcode/14608
- Determine CPUID:
  - `cpuid | grep "processor serial number =" | head -n1 | sed 's/.* = //;s/-0000.*//;s/-//'`
