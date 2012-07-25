%define name    microcode_ctl
%define version 1.03
%define release 1
%define serial  1
%define prefix  /usr

Summary:        Intel P6 CPU Microcode Utility
Name:           %{name}
Version:        %{version}
Release:        %{release}
Serial:         %{serial}
Group:          System Environment/Base
Copyright:      GPL
Url:            http://www.urbanmyth.org/microcode/
Vendor:         Simon Trimmer <simon@veritas.com>
Source:         %{name}-%{version}.tar.gz
Buildroot:      /var/tmp/%{name}-%{version}-root

%description
The microcode_ctl utility is a companion to the P6 microcode driver written
by Tigran Aivazian <tigran@veritas.com>. The utility has two uses:

a) it decodes and sends new microcode to the kernel driver to be uploaded
   to Intel P6 family processors. (Pentium Pro, PII, Celeron, PIII, Xeon etc)
b) it signals the kernel driver to release any buffers it may hold

The microcode update is volatile and needs to be uploaded on each system
boot i.e. it doesn't reflash your cpu permanently, reboot and it reverts
back to the old microcode.

%prep

%setup -q

%build
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -r $RPM_BUILD_ROOT;
make DESTDIR=$RPM_BUILD_ROOT PREFIX=%{prefix} install device clean

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -r $RPM_BUILD_ROOT;

%files
%defattr(-,root,root)
%{prefix}/sbin/microcode_ctl
%{prefix}/man/*/*
/etc/microcode.dat
/etc/rc.d/init.d/*
/etc/rc.d/rc3.d/*
/dev/cpu/microcode

%changelog
* Wed Sep  6 2000 Simon Trimmer <simon@veritas.com>
- Initial RPM
