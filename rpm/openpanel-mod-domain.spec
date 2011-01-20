%define 	modname	Domain

Name: 		openpanel-mod-domain
Version: 	1.0
Release: 	1%{?dist}
Summary:  	OpenPanel module to manage DNS and domains
License: 	GPLv3
Group: 		Applications/Internet
Source: 	%{name}-%{version}.tar.bz2
Requires:	openpanel-core
Requires: 	bind >= 9.3
BuildRequires:	openpanel-core-devel
BuildRequires:	grace-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
OpenPanel module to manage DNS and domains

%prep
%setup -q -n %{modname}.module
# nothing to configure

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_localstatedir}/openpanel/conf/staging/%{modname}
mkdir -p %{buildroot}/%{_localstatedir}/openpanel/modules/%{modname}.module/
cp -a *.png *.html *.def %{buildroot}/%{_localstatedir}/openpanel/modules/%{modname}.module/
cp -a action verify %{buildroot}/%{_localstatedir}/openpanel/modules/%{modname}.module/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %attr(-,openpanel-core, openpanel-authd) %{_localstatedir}/openpanel/conf/staging/%{modname}
%attr(-,openpanel-core, openpanel-authd) %{_localstatedir}/openpanel/modules/%{modname}.module

%post
/sbin/service openpaneld condrestart /dev/null 2>&1

%preun
if [ $1 = 0 ]; then
	service openpaneld stop >/dev/null 2>&1
fi

%postun
if [ $1 = 0 ]; then
	service openpaneld start >/dev/null 2>&1
fi
if [ "$1" = "1" ]; then
	service openpaneld condrestart >/dev/null 2>&1
fi

%changelog
* Wed Jan 18 2011 Igmar Palsenberg <igmar@palsenberg.com>
- Initial packaging
