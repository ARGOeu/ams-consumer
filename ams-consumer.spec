Name: ams-consumer
Summary: A/R Comp Engine message consumer
Version: 0.1.0
Release: 1%{?dist}
License: ASL 2.0
Buildroot: %{_tmppath}/%{name}-buildroot
Group:     EGI/SA4
BuildArch: noarch
Source0:   %{name}-%{version}.tar.gz
Requires: avro
Requires: argo-ams-library
Requires: python-daemon

%description
Installs the service for consuming SAM monitoring results
from the EGI message broker infrastructure.

%build
python setup.py build

%prep
%setup -n %{name}-%{version}

%install 
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory %{buildroot}/etc/init.d
install --directory %{buildroot}/etc/ams-consumer/
install --directory %{buildroot}/%{_sharedstatedir}/ams-consumer/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0755,root,root) /usr/bin/ams-consumerd
%attr(0755,root,root) /etc/init.d/ams-consumer
%attr(0750,arstats,arstats) %{_sharedstatedir}/ams-consumer

%post
/sbin/chkconfig --add ams-consumer

%pre
getent group arstats > /dev/null || groupadd -r arstats
getent passwd arstats > /dev/null || \
    useradd -r -g arstats -d /var/lib/ams-consumer -s /sbin/nologin \
    -c "AR Comp Engine user" arstats

%preun
if [ "$1" = 0 ] ; then
   /sbin/service ams-consumer stop
   /sbin/chkconfig --del ams-consumer
fi

%changelog
* Tue Feb 20 2018 Daniel Vrcic <dvrcic@srce.hr> - 0.1.0-1%{?dist}
- RPM package
