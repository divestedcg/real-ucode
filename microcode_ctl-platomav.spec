Summary:        Intel microcode files from Platomav's repository
Name:           microcode_ctl-platomav
Version:        20190624
Release:        2
Group:          System Environment/Base
License:        GPLv2+ and Redistributable, no modification permitted
Buildroot:      %{_tmppath}/%{name}-%{version}-root
ExclusiveArch:  %{ix86} x86_64

%description
Supports older systems

%install
mkdir -p %{buildroot}/lib/firmware/intel-ucode
iucode_tool --write-firmware=%{buildroot}/lib/firmware/intel-ucode/ platomav || true
#install -Dm644 platomav-converted/* %{buildroot}/lib/firmware/intel-ucode/

%files
/lib/firmware/*
