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

- AMD largely only provides direct microcode updates for enterprise platforms. Many consumer platforms only get microcode updates via AGESA updates.
  - Direct microcode updates are hot-loadable offering minimal downtime.
  - AGESA updates would require eg. the shuffling of virtual machines to another system and a reboot of the host.
- AMD actively delays updates to consumer systems by 2-3 months
  - This is before the delay from vendors providing system/motherboard updates

| bulletin | publication date | earliest enterprise microcode | earliest consumer agesa |
| -------- | ---------------- | ---------------------------- | ----------------------- |
| [AMD-SB-7005](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7005.html) | 2023-08-08 | 2023-06-09 | 2023-08-22 |
| [AMD-SB-7008](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7008.html) | 2023-07-24 | 2023-06-06 | 2023-11-21 |
| [AMD-SB-7014](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-7014.html) | 2024-08-09 | 2024-05-03 | 2024-07-30 |

Vendor Negligence
-----------------
> However, silly people carve out random microcode blobs from BIOS packages and think are doing other people a service this way...

I as of 2025-04-10 have 8 unique Zen1-4 AMD machines: Only 2 of them have been patched against CVE-2024-56161 despite being some 90 days old now, 3 of them have received an update in 2025, 3 in 2024, 1 in 2023, and 1 in 2021. Those last 5 are actively vulnerable to multiple known exploits purely because they haven't received vendor updates, but can be (partially) mitigated by simply loading the latest microcode as available from this repo. This is the direct blame of the vendors, but also the direct blame of Intel and AMD for only making the situation worse with their selective releases.

Stats (2025-11-13)
------------------
| provider | # supported cpuids | # outdated |
| -------- | ------------------ | ---------- |
| [Intel (official)](https://github.com/intel/Intel-Linux-Processor-Microcode-Data-Files/) | 286 | 42 |
| Intel (real-ucode) | 618 | 2 |
| [AMD (linux-firmware)](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/amd-ucode) | 48 | 28 |
| AMD (real-ucode) | 113 | 3 |

Stats (alternate) (2025-04-10)
------------------------------
- Intel has provided roughly 39 updates over the past 6 years.
- AMD has provided roughly 24 updates over the past 12 years.
- real-ucode has provided roughly 69 updates over the past 1.5 years.

Compatibility
-------------
- CentOS 9/Stream
- Fedora 38/39/40/41/42/etc.

License
-------
- See the LICENSE file

Prebuilts
---------
- Fedora via Divested-RPM: https://divested.dev/index.php?page=software#divested-release

Special AMD Incompatibility Notice (2025-03-02)
-----------------------------------------------
- After the recent AMD microcode signature verification vulnerability (CVE-2024-56161), microcode dated after 2024-11 will fail to load on pre 2025-01 bioses
- We can utilize the vulnerability to resign new ucodes for the old loaders: `sudo dnf swap amd-ucode-firmware amd-ucode-firmware-resigned`
- Hash check MUST be disabled: `sudo grubby --update-kernel=ALL --args="microcode.amd_sha_check=off"`
   - This evidently taints the kernel
- Closely watch your vendor for new bios updates
- These may fail to load upon resume from suspend when using s3 sleep, please use s2idle instead

Usage
-----
- Once Divested-RPM is installed, simply running `dnf update` will pull in our `amd-ucode-firmware` and `microcode_ctl` packages due to their higher epoch version
- Alternatively build them yourself and install them manually
- Regenerate initramfs: `dracut -f`
- Reboot
- Verify
   - If it fails then disable the hash check: `sudo grubby --update-kernel=ALL --args="microcode.amd_sha_check=off"`

Verifying it took
-----------------
- You can do this a few ways:
  - Checking logs, eg. `journalctl -b0 | grep -i microcode` then `-b-1`
  - Less reliable, running `lscpu` before and after, then diffing

Building
--------
- git clone [THIS REPO]
- CentOS: rpmbuild -ba real-ucode.spec
- Fedora: rpmbuild -ba real-ucode.spec

Preparing
---------
- git clone [THIS REPO]
- git clone https://github.com/platomav/CPUMicrocodes
- git clone https://github.com/AndyLavr/amd-ucodegen
- git clone https://github.com/google/security-research
- mkdir compiled
- cd security-research/pocs/cpus/entrysign/zentool
- sudo dnf install pkg-config gmp-devel json-c-devel openssl-devel libasan nasm dwarves
- make
- cp zentool ../../../../../compiled/
- cd ../../../../../
- cd amd-ucodegen
- git apply ../amd-ucodegen-tweak.diff
- make
- cp amd-ucodegen ../compiled/
- cd ..

Maintaining this repo
---------------------
- cd CPUMicrocodes
- git pull
- sh ../process-intel.sh
- sh ../process-amd-official.sh
- sh ../process-amd-resigned.sh
- git add -A && git reset --hard
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
- There is an ALT Linux port by @vt-alt:
  - https://github.com/altlinux/specs/blob/sisyphus/r/real-ucode/real-ucode.spec
- There is an Arch Linux port on the AUR by @moparisthebest:
  - https://aur.archlinux.org/packages/amd-real-ucode-git
  - https://aur.archlinux.org/packages/intel-real-ucode-git
- There is a similar project for NixOS here: https://github.com/e-tho/ucodenix
- Forum threads for this are here:
  - https://winraid.level1techs.com/t/real-ucode-all-the-microcodes-but-packaged/103179
  - https://discuss.privacyguides.net/t/real-ucode-a-fedora-package-with-all-the-microcode/14608
- Determine CPUID:
  - `cpuid | grep "processor serial number =" | head -n1 | sed 's/.* = //;s/-0000.*//;s/-//'`
