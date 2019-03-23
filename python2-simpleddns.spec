%include %{_rpmconfigdir}/macros.python

%global debug_package %{nil}
%define proj_name simpleddns
%define _release 1

Name:           python2-%{simpleddns}
Version:        1.0.0
Release:        %{_release}%{?dist}
Summary:        ddns utils
Group:          Development/Libraries
License:        MPLv1.1 or GPLv2
URL:            http://github.com/Lolizeppelin/%{proj_name}
Source0:        %{proj_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python >= 2.7
BuildRequires:  python2-setuptools >= 40

Requires:       python >= 2.7
Requires:       python < 3.0
Requires:       python-netaddr >= 0.7.5


%description
A simple ddns util

%prep
%setup -q -n %{proj_name}-%{version}
rm -rf %{proj_name}.egg-info

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}


%pre
if [ "$1" = "1" ] ; then
    getent group ddns >/dev/null || groupadd -f -g 874 -r ddns
    if ! getent passwd ddns >/dev/null ; then
        if ! getent passwd 874 >/dev/null ; then
          useradd -r -u 874 -g ddns -M -s /sbin/nologin -c "Ddns server" ddns
        else
          useradd -r -g ddns -M -s /sbin/nologin -c "Ddns user" ddns
        fi
    fi
fi


%postun
if [ "$1" = "0" ] ; then
    /usr/sbin/userdel ddns > /dev/null 2>&1
fi


%files
%defattr(-,root,root,-)
%{py_sitedir}/%{proj_name}/*
%dir %{py_sitedir}/%{proj_name}-%{version}-*.egg-info/
%{py_sitedir}/%{proj_name}-%{version}-*.egg-info/*
#%{py_sitedir}/%{proj_name}/*
#%{python2_sitearch}/%{proj_name}/*
#%{python2_sitearch}/%{proj_name}-%{version}-*.egg-info/*
#%dir %{python2_sitearch}/%{proj_name}-%{version}-*.egg-info/
%doc README.rst
%doc doc/*

%changelog
* Fri Mar 15 2019 Lolizeppelin <lolizeppelin@gmail.com> - 1.0.0
- Initial Package