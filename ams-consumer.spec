Name:          argo-ams-consumer
Summary:       Argo Messaging System metric results consumer
Version:       0.1.0
Release:       1%{?dist}
License:       ASL 2.0

BuildArch:     noarch
BuildRequires: python2-devel
Buildroot:     %{_tmppath}/%{name}-buildroot
Requires:      argo-ams-library
Requires:      avro
Requires:      python-daemon
Source0:       %{name}-%{version}.tar.gz

%description
AMS consumer fetchs metric results from Argo Messaging System and stores them
in avro serialized files

%build
python setup.py build

%prep
%setup -n %{name}-%{version}

%install 
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory %{buildroot}/etc/init.d
install --directory %{buildroot}/etc/argo-ams-consumer/
install --directory %{buildroot}/%{_sharedstatedir}/argo-ams-consumer/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%attr(0755,root,root) /usr/bin/ams-consumerd
%attr(0755,root,root) /etc/init.d/ams-consumer
%attr(0750,root,root) %{_sharedstatedir}/argo-ams-consumer

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
