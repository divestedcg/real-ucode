Name: real-ucode
Version: 20251219
Release: 1
Epoch: 3
Summary: Actually provides the latest CPU microcode for AMD and Intel
License: proprietary
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: amd-ucode-firmware >= 3:20231101
Requires: microcode_ctl >= 3:20231101
%define _binary_payload w3T.xzdio
%define _sourcedir %(echo $PWD)
%define _rpmdir %(echo $PWD/build)

%description
Please see the included README

%package -n amd-ucode-firmware
Summary: Latest microcode for AMD
License: Redistributable, no modification permitted
Requires: linux-firmware-whence
RemovePathPostfixes: .official
%description -n amd-ucode-firmware
Microcode updates for AMD CPUs.

%post -n amd-ucode-firmware
echo "ucode hash check LIKELY needs to be disabled: sudo grubby --update-kernel=ALL --args=\"microcode.amd_sha_check=off\"";

%package -n amd-ucode-firmware-resigned
Summary: Latest microcode for AMD, resigned
License: Redistributable, no modification permitted
Requires: linux-firmware-whence
RemovePathPostfixes: .resigned
Provides: amd-ucode-firmware
%description -n amd-ucode-firmware-resigned
Microcode updates for AMD CPUs, resigned for vulnerable loaders.

%post -n amd-ucode-firmware-resigned
echo "ucode hash check MUST be disabled: sudo grubby --update-kernel=ALL --args=\"microcode.amd_sha_check=off\"";

%package -n microcode_ctl
Summary: Latest microcode for Intel
License: Redistributable, no modification permitted
Requires: linux-firmware-whence
%description -n microcode_ctl
Microcode updates for Intel CPUs.

%install
mkdir -p %{buildroot}/usr/lib/firmware/amd-ucode/;
install -Dm644 %{_sourcedir}/microcode/amd-ucode/* %{buildroot}/usr/lib/firmware/amd-ucode/;
mkdir -p %{buildroot}/usr/lib/firmware/intel-ucode/;
install -Dm644 %{_sourcedir}/microcode/intel-ucode/* %{buildroot}/usr/lib/firmware/intel-ucode/;
install -Dm644 %{_sourcedir}/README.md %{buildroot}/usr/share/doc/real-ucode/README.md;

%files
/usr/share/doc/real-ucode/README.md

%files -n amd-ucode-firmware
/usr/lib/firmware/amd-ucode/LICENSE.amd-ucode
/usr/lib/firmware/amd-ucode/*.bin.official

%files -n amd-ucode-firmware-resigned
/usr/lib/firmware/amd-ucode/LICENSE.amd-ucode
/usr/lib/firmware/amd-ucode/*.bin.resigned

%files -n microcode_ctl
/usr/lib/firmware/intel-ucode/*
