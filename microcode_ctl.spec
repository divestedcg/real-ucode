%define name    microcode_ctl
%define version 1.05
%define release 1
%define serial  1
%define prefix  /usr

Summary:        Intel IA32 CPU Microcode Utility
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
The microcode_ctl utility is a companion to the IA32 microcode driver written
by Tigran Aivazian <tigran@veritas.com>. The utility has two uses:

a) it decodes and sends new microcode to the kernel driver to be uploaded
   to Intel IA32 family processors. (Pentium Pro, PII, Celeron, PIII, Xeon
   Pentium 4 etc.)
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
/dev/cpu/microcode

%post
if [ -x /sbin/chkconfig ];
then
	chkconfig --add microcode_ctl
elif [ -f /etc/SuSE-release ];
then
	# XXX is there a better way to do this under SuSE?
	ln -s ../microcode_ctl /sbin/init.d/rc2.d/S80microcode_ctl
	ln -s ../microcode_ctl /sbin/init.d/rc2.d/K20microcode_ctl
else
	echo "RPM: Unknown system, leaving system startup alone"
fi

%preun
if [ -x /sbin/chkconfig ];
then
	chkconfig --del microcode_ctl
elif [ -f /etc/SuSE-release ];
then
	rm -f /sbin/init.d/rc2.d/S80microcode_ctl
	rm -f /sbin/init.d/rc2.d/K20microcode_ctl
fi
