Summary:        Tool to update x86/x86-64 CPU microcode.
Name:           microcode_ctl
Version:        1.18
Release:        1
Group:          System Environment/Base
License:        GPLv2+ and Redistributable, no modification permitted
URL:            http://fedorahosted.org/microcode_ctl
Source0:        http://fedorahosted.org/released/microcode_ctl/%{name}-%{version}.tar.xz
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Requires:       udev
Requires(pre):  /sbin/chkconfig /sbin/service
Requires(pre):  grep gawk coreutils
ExclusiveArch:  %{ix86} x86_64

%description
The microcode_ctl utility is a companion to the microcode driver written
by Tigran Aivazian <tigran@aivazian.fsnet.co.uk>. 

The microcode update is volatile and needs to be uploaded on each system
boot i.e. it doesn't reflash your cpu permanently, reboot and it reverts
back to the old microcode.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} \
	INSDIR=/usr/sbin MANDIR=%{_mandir}/man8 install clean

%clean
rm -rf %{buildroot}

%files
/usr/sbin/microcode_ctl
/etc/init.d/microcode_ctl
/lib/firmware/*
%doc /usr/share/doc/microcode_ctl/*
%attr(0644,root,root) %{_mandir}/*/*

%post
if [ -x /sbin/chkconfig ];
then
	chkconfig --add microcode_ctl
else
	echo "RPM: Unknown system, leaving system startup alone"
fi

%preun
if [ -x /sbin/chkconfig ];
then
	chkconfig --del microcode_ctl
fi

