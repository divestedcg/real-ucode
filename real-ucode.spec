Name: real-ucode
Version: 20240115
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
%description -n amd-ucode-firmware
Microcode updates for AMD CPUs.

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
/usr/lib/firmware/amd-ucode/*

%files -n microcode_ctl
/usr/lib/firmware/intel-ucode/*
