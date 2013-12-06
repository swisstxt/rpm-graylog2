Name:           graylog2-web-interface
Version:        %{ver}
Release:        %{rel}%{?dist}
Summary:        Graylog2 web interface
BuildArch:      x86_64
Group:          Application/Internet
License:        GPLv3
URL:            https://graylog2.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: opt-ruby-1.9.3 opt-ruby-1.9.3-rubygem-bundler
BuildRequires: gcc libxml2 ruby-devel libxml2-devel libxslt libxslt-devel

%define appdir /var/www/vhosts/%{name}
%define configdir %{appdir}/config
%define logdir %{appdir}/log
%define tmpdir %{appdir}/tmp


%description
Graylog2 web interface

%prep

%build
pushd %{name}
  /opt/ruby-1.9.3/bin/bundle install --deployment

	cat <<-EOD > gemrc
    gemhome: $PWD/vendor/bundle/ruby/1.9.3
    gempath:
    - $PWD/vendor/bundle/ruby/1.9.3
EOD

  /opt/ruby-1.9.3/bin/gem --config-file ./gemrc install bundler
	rm ./gemrc
popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{logdir}
mkdir -p $RPM_BUILD_ROOT/%{tmpdir}
mkdir -p $RPM_BUILD_ROOT/%{configdir}

pushd %{name}
  mv config/mongoid.yml.example config/mongoid.yml
	mv app config* lib public script vendor \
    Rakefile README Gemfile* \
    $RPM_BUILD_ROOT/%{appdir}
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{appdir}
%attr(755,apache,apache) %{logdir}
%attr(755,nobody,nobody) %{tmpdir}
%doc
