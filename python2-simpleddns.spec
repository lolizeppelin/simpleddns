%include %{_rpmconfigdir}/macros.python

%global debug_package %{nil}
%define proj_name simpleddns
%define _release 12

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
Requires:       rp-pppoe >= 3.0
Requires:       python2-netaddr >= 0.7.5
Requires:       python2-psutil >= 5.0
Requires:       python2-requests >= 2.2


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
mkdir -p %{buildroot}%{_sharedstatedir}/%{proj_name}

%{__install} -D -m 0640 -p etc/%{proj_name}/ddns.conf -t %{buildroot}%{_sysconfdir}/%{proj_name}
%{__install} -D -m 0644 -p ddns.service %{buildroot}%{_unitdir}/ddns.service
%{__install} -D -m 0644 -p ddns.timer %{buildroot}%{_unitdir}/ddns.timer

for l in bin/*;do
    %{__install} -D -m 0755 $l -t %{buildroot}%{_bindir}
done;


%pre
if [ "$1" = "1" ] ; then
    getent group ddns >/dev/null || groupadd -f -g 874 -r ddns
    if ! getent passwd ddns >/dev/null ; then
        if ! getent passwd 874 >/dev/null ; then
          useradd -r -u 874 -g ddns -M -s /sbin/nologin -c "Ddns process user" ddns
        else
          useradd -r -g ddns -M -s /sbin/nologin -c "Ddns process user" ddns
        fi
    fi
fi



%preun
systemctl stop ddns.timer

%postun
if [ "$1" = "0" ] ; then
    /usr/sbin/userdel ddns > /dev/null 2>&1
fi



%files
%defattr(-,root,root,-)
%{_bindir}/ddns-notify
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
%defattr(-,ddns,ddns,-)
%dir %{_sharedstatedir}/%{proj_name}
%config(noreplace) %{_sysconfdir}/%{proj_name}/ddns.conf

%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package