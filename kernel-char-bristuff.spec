#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
#

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	0.1
%define		ver	0.3.0-PRE-1y-k
%define		ver2	%(echo %ver | tr '-' '_')

Summary:	Linux driver for bristuff
Summary(pl.UTF-8):	Sterownik linuksa do bristuff
Name:		kernel%{_alt_kernel}-char-bristuff
Version:	%{ver2}
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://212.91.251.199/~junghanns.net/downloads/bristuff-%{ver}.tar.gz
# Source0-md5:	2c45a1955703b7f208310a9dd0a6b1f1
URL:		http://212.91.251.199/~junghanns.net/downloads/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
Buildrequires:	zaptel-devel(bristuff)
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is driver for bristuff for Linux.

This package contains Linux module.

%description -l pl.UTF-8
Sterownik dla Linuksa do bristuff.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n bristuff-%{ver}
for i in ztgsm qozap cwain zaphfc;
do
	echo "obj-m += $i.o" > $i/Makefile
	echo "CFLAGS += -I/usr/include/zaptel" >> $i/Makefile
done

%build
%if %{with kernel}
	for i in ztgsm qozap cwain zaphfc;
	do
		%build_kernel_modules -C $i -m $i
	done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
	for i in ztgsm qozap cwain zaphfc;
	do
		cd $i
		%install_kernel_modules -m $i -d kernel/drivers/char
		cd ..
	done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-char-bristuff
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/char/*.ko*
%endif
