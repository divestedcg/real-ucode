Name: real-ucode
Version: 20231022
Release: 1
Summary: Actually provides the latest CPU microcode for AMD
License: proprietary
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%define _binary_payload w3T.xzdio
%define _sourcedir %(echo $PWD)
%define _rpmdir %(echo $PWD/build)

%description
Please see the included README

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
