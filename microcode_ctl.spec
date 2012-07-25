%define name    microcode_ctl
%define version 1.15
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
Vendor:         Simon Trimmer <simon@urbanmyth.org>
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
make DESTDIR=$RPM_BUILD_ROOT PREFIX=%{prefix} install clean

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -r $RPM_BUILD_ROOT;

%files -f microcode-filelist
%defattr(-,root,root)
%{prefix}/sbin/microcode_ctl
%{prefix}/man/*/*
/etc/microcode.dat
# /etc/init.d/microcode_ctl

%post
if [ ! -f /dev/.devfsd ];
then
	# devfs is not installed
	mkdir -p /dev/cpu
	if [ ! -c /dev/cpu/microcode ];
	then
		mknod /dev/cpu/microcode c 10 184
	fi
fi

if [ -x /sbin/chkconfig ];
then
	chkconfig --add microcode_ctl
elif [ -f /etc/SuSE-release ];
then
	# XXX is there a better way to do this under SuSE?
	if [ -d /etc/init.d ];
	then
		# Suse 7.1
		ln -s /etc/init.d/microcode_ctl /etc/init.d/rc2.d/S80microcode_ctl
		ln -s /etc/init.d/microcode_ctl /etc/init.d/rc2.d/K20microcode_ctl
	else
		# Suse 7.0, same style as Suse.
		ln -s ../microcode_ctl /etc/rc.d/rc2.d/S80microcode_ctl
		ln -s ../microcode_ctl /etc/rc.d/rc2.d/K20microcode_ctl
	fi
else
	echo "RPM: Unknown system, leaving system startup alone"
fi


%preun
if [ -x /sbin/chkconfig ];
then
	chkconfig --del microcode_ctl
elif [ -f /etc/SuSE-release ];
then
	if [ -d /etc/init.d ];
	then
		# Suse 7.1
		rm -f /etc/init.d/rc2.d/S80microcode_ctl
		rm -f /etc/init.d/rc2.d/K20microcode_ctl
	else
		# Suse 7.0
		rm -f /etc/rc.d/rc2.d/S80microcode_ctl
		rm -f /etc/rc.d/rc2.d/K20microcode_ctl
	fi
fi

if [ ! -f /dev/.devfsd ];
then
	rm -f /dev/cpu/microcode
	rmdir --ignore-fail-on-non-empty /dev/cpu
fi
