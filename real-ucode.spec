Name: real-ucode
Version: 20231022
Release: 2
Summary: Actually provides the latest CPU microcode for AMD
License: proprietary
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%define _binary_payload w3T.xzdio
%define _sourcedir %(echo $PWD)
%define _rpmdir %(echo $PWD/build)

%description
AMD appears to primarily only include microcode for enterprise platforms in the linux-firmware repo.
Intel also appears to miss a few and doesn't always include the latest available.
This contains all available microcodes thanks to the following projects:
https://github.com/platomav/CPUMicrocodes
https://github.com/AndyLavr/amd-ucodegen

%post
echo "Be sure to run install-real-ucode and again after each linux-firmware update!";

%install
mkdir -p %{buildroot}/usr/lib/firmware/amd-ucode-real/;
install -Dm644 %{_sourcedir}/microcode/amd-ucode/microcode_amd_fam*.bin %{buildroot}/usr/lib/firmware/amd-ucode-real/;
#mkdir -p %{buildroot}/usr/lib/firmware/intel-ucode-real/;
#install -Dm644 %{_sourcedir}/microcode/intel-ucode/* %{buildroot}/usr/lib/firmware/intel-ucode-real/;
install -Dm755 %{_sourcedir}/install-real-ucode %{buildroot}/usr/sbin/install-real-ucode;

%files
/usr/lib/firmware/amd-ucode-real/microcode_amd_fam*.bin
#/usr/lib/firmware/intel-ucode-real/*
/usr/sbin/install-real-ucode
