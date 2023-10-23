Name: real-ucode
Version: 20231022
Release: 5
Summary: Actually provides the latest CPU microcode for AMD and Intel
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
install -Dm755 %{_sourcedir}/install-real-ucode %{buildroot}/usr/sbin/install-real-ucode;
mkdir -p %{buildroot}/usr/lib/firmware/amd-ucode-real/;
install -Dm644 %{_sourcedir}/microcode/amd-ucode/* %{buildroot}/usr/lib/firmware/amd-ucode-real/;
mkdir -p %{buildroot}/usr/lib/firmware/intel-ucode-real/;
install -Dm644 %{_sourcedir}/microcode/intel-ucode/* %{buildroot}/usr/lib/firmware/intel-ucode-real/;
install -Dm644 %{_sourcedir}/README.md %{buildroot}/usr/share/doc/real-ucode/README.md;

%files
/usr/lib/firmware/amd-ucode-real/*
/usr/lib/firmware/intel-ucode-real/*
/usr/sbin/install-real-ucode
/usr/share/doc/real-ucode/README.md
