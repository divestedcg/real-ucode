Name: real-ucode
Version: 20231021
Release: 1
Summary: Actually provides the latest CPU microcode for Intel and AMD
License: proprietary
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%define _binary_payload w3T.xzdio
%define _sourcedir %(echo $PWD)
%define _rpmdir %(echo $PWD/build)

%description
Please see the included README

%install
mkdir -p %{buildroot}/usr/lib/firmware/amd-ucode-real/;
install -Dm644 %{_sourcedir}/microcode/amd-ucode/microcode_amd_fam*.bin %{buildroot}/usr/lib/firmware/amd-ucode-real/;
#mkdir -p %{buildroot}/usr/lib/firmware/intel-ucode-real/;
#install -Dm644 %{_sourcedir}/microcode/intel-ucode/* %{buildroot}/usr/lib/firmware/intel-ucode-real/;

%files
/usr/lib/firmware/amd-ucode-real/microcode_amd_fam*.bin
#/usr/lib/firmware/intel-ucode-real/*
