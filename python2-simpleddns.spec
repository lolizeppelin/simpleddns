%include %{_rpmconfigdir}/macros.python

%global debug_package %{nil}
%define proj_name simpleddns
%define _release 1

Name:           python2-%{proj_name}
Version:        1.0.0
Release:        %{_release}%{?dist}
Summary:        ddns utils
Group:          Development/Libraries
License:        MPLv1.1 or GPLv2
URL:            http://github.com/Lolizeppelin/%{proj_name}
Source0:        %{proj_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2 >= 2.7
BuildRequires:  python2-setuptools >= 40

Requires:       python2 >= 2.7
Requires:       rp-pppoe < 3.0
Requires:       python2-netaddr >= 0.7.5


%description
A simple ddns util

%prep
%setup -q -n %{proj_name}-%{version}
rm -rf %{proj_name}.egg-info

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/%{proj_name}

%{__install} -D -m 0644 -p etc/%{proj_name}/ddns.conf -t %{buildroot}%{_sysconfdir}/%{proj_name}
%{__install} -D -m 0644 -p ddns.service %{buildroot}%{_unitdir}/ddns.service
%{__install} -D -m 0644 -p ddns.timer %{buildroot}%{_unitdir}/ddns.timer

for l in sbin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_sbindir}
done;

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{proj_name}/ddns.conf
%{_sbindir}/ddns-notify
%{_unitdir}/ddns.service
%{_unitdir}/ddns.timer
%{py_sitedir}/%{proj_name}/*
%dir %{py_sitedir}/%{proj_name}-%{version}-*.egg-info/
%{py_sitedir}/%{proj_name}-%{version}-*.egg-info/*
#%{py_sitedir}/%{proj_name}/*
#%{python2_sitearch}/%{proj_name}/*
#%{python2_sitearch}/%{proj_name}-%{version}-*.egg-info/*
#%dir %{python2_sitearch}/%{proj_name}-%{version}-*.egg-info/
%doc README.rst

%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package