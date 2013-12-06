# $Id: graylog2-server.spec 159 2010-10-25 11:11:35Z mrugesh $
# Spec file for graylog2 server

# Various paths
%global         graylog2_installdir   %{_datadir}/%{name}
%global         graylog2_logdir       %{_localstatedir}/log/%{name}
%global         graylog2_config       %{_sysconfdir}/graylog2.conf
%global         graylog2_service      %{_initrddir}/%{name}

Name:           graylog2-server
Version:        %{ver}
Release:        %{rel}%{?dist}

Summary:        A syslog implementation that stores logs in MongoDB

Group:          System Environment/Daemons
License:        GPLv3
URL:            http://www.graylog2.org

Source0:        http://github.com/downloads/lennartkoopmann/graylog2-server/%{name}-%{version}.tar.gz
Source1:        graylog2-server.init

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       jpackage-utils
Requires:       java >= 1:1.6.0

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts


%description

Graylog2 is an open source syslog implementation that stores logs
in MongoDB. It consists of a server written in Java that accepts
syslog messages via TCP or UDP and stores them in the database.


%prep
%setup -q


%build


%install
rm -rf %{buildroot}

# Install the application
mkdir -p %{buildroot}%{graylog2_installdir}
install -m 644 graylog2-server.jar %{buildroot}%{graylog2_installdir}/%{name}.jar
ln -s %{graylog2_installdir}/%{name}.jar %{buildroot}%{graylog2_installdir}/%{name}-%{version}.jar

# Install the config file
mkdir -p %{buildroot}%{_sysconfdir}
install -m 640 graylog2.conf.example %{buildroot}%{graylog2_config}

# Install the init script
mkdir -p %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{graylog2_service}

# Create the log directory
mkdir -p %{buildroot}%{graylog2_logdir}


%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add %{name}


%preun
if [[ $1 = 0 ]]
then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi


%postun
if [[ $1 -ge 1 ]]
then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING graylog2.conf.example build_date
%{graylog2_installdir}
%config(noreplace) %{graylog2_config}
%dir %{graylog2_logdir}
%{graylog2_service}


%changelog
* Thu Mar 07 2013 Mrugesh Karnik <mrugesh@brainfunked.org> - 0.11.0-1
- bump version
* Mon Oct 25 2010 Mrugesh Karnik <mrugesh@brainfunked.org> - 0.9.3-1
- Initial package
