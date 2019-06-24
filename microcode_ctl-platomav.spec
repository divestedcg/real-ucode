Summary:        Intel microcode files from Platomav's repository
Name:           microcode_ctl-platomav
Version:        20190624
Release:        7
Group:          System Environment/Base
License:        GPLv2+ and Redistributable, no modification permitted
Buildroot:      %{_tmppath}/%{name}-%{version}-root
ExclusiveArch:  %{ix86} x86_64

%description
Supports older systems

%install
mkdir -p %{buildroot}/lib/firmware/intel-ucode
install -Dm644 intel-ucode/* %{buildroot}/lib/firmware/intel-ucode/
install -Dm644 intel-ucode-with-caveats/* %{buildroot}/lib/firmware/intel-ucode/
iucode_tool --overwrite --write-firmware=%{buildroot}/lib/firmware/intel-ucode/ platomav-ucode

%files
/lib/firmware/*
