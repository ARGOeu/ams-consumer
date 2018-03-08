%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%define underscore() %(echo %1 | sed 's/-/_/g')
%define stripc() %(echo %1 | sed 's/el7.centos/el7/')

%if 0%{?el7:1}
%define mydist %{stripc %{dist}}
%else
%define mydist %{dist}
%endif

Name:          argo-ams-consumer
Summary:       Argo Messaging Service metric results consumer
Version:       0.1.0
Release:       1%{?mydist}
License:       ASL 2.0

BuildArch:     noarch
BuildRequires: python2-devel
Buildroot:     %{_tmppath}/%{name}-buildroot
Requires:      argo-ams-library
Requires:      avro
Requires:      python-daemon

%if 0%{?el7:1}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires(post): systemd-sysv
%endif

Source0:       %{name}-%{version}.tar.gz

%description
AMS consumer fetchs metric results from Argo Messaging Service and stores them
in avro serialized files

%build
python setup.py build

%prep
%setup -n %{name}-%{version}

%install 
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory %{buildroot}/etc/%{name}/
install --directory %{buildroot}/%{_sharedstatedir}/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/run/%{name}/
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}/

%if 0%{?el7:1}
sed -i "/\/etc\/init.d\/ams-consumer/d" INSTALLED_FILES
rm %{buildroot}/etc/init.d/ams-consumer
%else
sed -i "/\/usr\/lib\/systemd\/system\//d" INSTALLED_FILES
rm %{buildroot}/usr/lib/systemd/system/ams-consumer.service 
%endif

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0755,root,root) /usr/bin/ams-consumerd
%attr(0750,root,root) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/ams-consumer.conf 
%dir %{python_sitelib}/%{underscore %{name}}
%{python_sitelib}/%{underscore %{name}}/*.py[co]
%dir %{_localstatedir}/log/%{name}/
%dir %{_localstatedir}/run/%{name}/

%if 0%{?el7:1}
%{_unitdir}/ams-consumer.service
%else
%attr(0755,root,root) /etc/init.d/ams-consumer
%endif

%post
/sbin/chkconfig --add ams-consumer

%preun
if [ "$1" = 0 ] ; then
   /sbin/service ams-consumer stop
   /sbin/chkconfig --del ams-consumer
fi

%changelog
* Tue Feb 20 2018 Daniel Vrcic <dvrcic@srce.hr> - 0.1.0-1%{?dist}
- RPM package
