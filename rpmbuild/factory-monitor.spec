%{!?ver:          %define ver      0.1}
%{!?rel:          %define rel      1}
%{!?name:         %define name      factory-monitor}

Name:           %{name}
Version:        %{ver}
Release:        %{rel}
Summary: Visualizes Condor Factory meta data in Grafana
License: Apache 2.0

Source0:	%{name}-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:  noarch

Requires: python

%description
This monitor aggregates data accumulated by the factory and sends it to a database
to be visualized by Grafana. At the time of this writing, the database in use is
InfluxDB.

%pre
getent group factmon >/dev/null || groupadd -r GROUPNAME
getent passwd factmon >/dev/null || \
    useradd -r -g factmon -d HOMEDIR -s /sbin/nologin \
    -c "this user is created to allow for selective use of the service" factmon
exit 0

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/var/lib/factory-monitor/{aggregator,config,http,messenger/outbox,crontab}
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/etc/cron.d
mkdir -p %{buildroot}/etc/logrotate.d

install -m 777 init.d/factory-monitor %{buildroot}/etc/init.d/
install -m 777 logrotate/factory-monitor %{buildroot}/etc/logrotate.d/
install -m 644 crontab/factory-monitor %{buildroot}/var/lib/factory-monitor/crontab/
install -m 777 monitor.py %{buildroot}/var/lib/factory-monitor/
install -m 777 aggregator/*.py %{buildroot}/var/lib/factory-monitor/aggregator/
install -m 777 config/*.py %{buildroot}/var/lib/factory-monitor/config/
install -m 777 config/config.json %{buildroot}/var/lib/factory-monitor/config/
install -m 777 http/*.py %{buildroot}/var/lib/factory-monitor/http/
install -m 777 messenger/*.py %{buildroot}/var/lib/factory-monitor/messenger/

%postun
if [ "$1" = "0" ] ; then #Remove package
  rm -rf /var/lib/factory-monitor
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/etc/init.d/factory-monitor
/etc/logrotate.d/factory-monitor
/var/lib/factory-monitor/crontab/factory-monitor
/var/lib/factory-monitor/monitor.py*
/var/lib/factory-monitor/aggregator/*.py*
/var/lib/factory-monitor/config/*.py*
%config(noreplace) /var/lib/factory-monitor/config/config.json
/var/lib/factory-monitor/http/*.py*
/var/lib/factory-monitor/messenger/*.py*

%dir /var/lib/factory-monitor/aggregator/
%dir /var/lib/factory-monitor/config/
%dir /var/lib/factory-monitor/http/
%dir /var/lib/factory-monitor/messenger/
%dir /var/lib/factory-monitor/messenger/outbox/

