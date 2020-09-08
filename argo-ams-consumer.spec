%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%define underscore() %(echo %1 | sed 's/-/_/g')
%define stripc() %(echo %1 | sed 's/el7.centos/el7/')
%define mydist %{stripc %{dist}}

Name:          argo-ams-consumer
Summary:       Argo Messaging Service metric results consumer
Version:       2.0.0
Release:       1%{?mydist}
License:       ASL 2.0

BuildArch:     noarch
BuildRequires: python3-devel python3-setuptools
Buildroot:     %{_tmppath}/%{name}-buildroot
Requires:      python3-argo-ams-library
Requires:      python3-avro

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(post):   systemd-sysv

Source0:       %{name}-%{version}.tar.gz

%description
AMS consumer fetchs metric results from Argo Messaging Service and stores them
in avro serialized files

%build
%{py3_build}

%prep
%setup -q

%install
rm -rf %{buildroot}
%{py3_install "--record=INSTALLED_FILES"}
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_sharedstatedir}/%{name}/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0755,root,root) /usr/bin/ams-consumerd
%attr(0755,root,root) %{_sharedstatedir}/%{name}
%dir %{_localstatedir}/log/%{name}/
%dir %{_localstatedir}/run/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/ams-consumer.conf
%{_unitdir}/ams-consumer@.service
%{_unitdir}/ams-consumers.target
%{python3_sitelib}/*

%post
%systemd_post ams-consumers.target

%postun
%systemd_postun_with_restart ams-consumers.target

%preun
%systemd_preun ams-consumers.target

%changelog
* Tue Sep 8 2020 Daniel Vrcic <dvrcic@srce.hr> - 2.0.0-1%{?dist}
- ARGO-2080 Refactor AMS clients to use retry ams-library feature
- ARGO-2261 ams-consumer retry on ack_sub also
- ARGO-2513 Drop Centos6/Python2 support
- ARGO-2527 Use systemd instances for spawning of multiple tenant ams-consumers
* Fri Nov 8 2019 Daniel Vrcic <dvrcic@srce.hr>, Konstantinos Kagkelidis <kaggis@gmail.com> - 1.1.0-1%{?dist}
- Fix dash typo in consumer systemd service file
- ARGO-1262 Extend consumer schema with actual_data field
* Thu May 10 2018 Daniel Vrcic <dvrcic@srce.hr>, Hrvoje Sute <hsute@srce.hr> - 1.0.0-1%{?dist}
- ARGO-1106 Pull interval as float
- ARGO-1092 AMS Consumer README
- ARGO-1069 AMS Consumer Centos7 support
- ARGO-1050 Connection timeout as config option
- ARGO-869 RPM packaging metadata
- ARGO-1036 report period fix
- ARGO-1036 Message retention logic
- ARGO-790 avro serialization of fetched data
- ARGO-971 AMS messages fetching loop
- ARGO-846 Introduce config parser with template config file
- ARGO-845 Daemonize worker process and register signal handlers
* Tue Feb 20 2018 Daniel Vrcic <dvrcic@srce.hr> - 0.1.0-1%{?dist}
- RPM package
