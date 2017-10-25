# Define Constants
%define name exchange
%define _version 1.3.0
%define _release 1
%define _branch master

%if %{?ver:1}0
%define version %{ver}
%else
%define version %{_version}
%endif

%if %{?rel:1}0
%define release %{rel}
%else
%define release %{_release}
%endif

%if %{?commit:1}0
%define branch %{commit}
%else
%define branch %{_branch}
%endif

%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:             %{name}
Version:          %{version}
Release:          %{release}%{?dist}
Summary:          Boundless Exchange, Web GIS for Everyone
Group:            Applications/Engineering
License:          GPLv3
Packager:         BerryDaniel <dberry@boundlessgeo.com>
Source0:          supervisord.conf
Source1:          %{name}.init
%{?el6:Source2: %{name}-el6.conf}
%{?el6:Source3: proxy-el6.conf}
%{?el7:Source2: %{name}-el7.conf}
%{?el7:Source3: proxy-el7.conf}
Source4:          settings.py
Source5:          %{name}-config
Source6:          celery-worker.sh
Source7:          waitress.sh
Source8:          %{name}-settings.sh
Source9:          manage.py
Source10:         wsgi.py
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
%{?el6:BuildRequires: python27-devel}
%{?el6:BuildRequires: python27-virtualenv}
%{?el7:BuildRequires: python-devel}
%{?el7:BuildRequires: python-virtualenv}
BuildRequires:    boundless-vendor-libs
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    make
BuildRequires:    expat-devel
BuildRequires:    gdbm-devel
BuildRequires:    sqlite-devel
BuildRequires:    readline-devel
BuildRequires:    zlib-devel
BuildRequires:    bzip2-devel
BuildRequires:    openssl-devel
BuildRequires:    openldap-devel
BuildRequires:    tk-devel
BuildRequires:    libxslt-devel
BuildRequires:    libxml2-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    zlib-devel
BuildRequires:    libtiff-devel
BuildRequires:    freetype-devel
BuildRequires:    libmemcached-devel
BuildRequires:    unzip
BuildRequires:    git
%{?el6:Requires: python27}
%{?el6:Requires: python27-virtualenv}
%{?el7:Requires: python}
%{?el7:Requires: python-virtualenv}
Requires:         boundless-vendor-libs
Requires:         httpd
Requires:         mod_ssl
Requires:         openldap
Requires:         libxslt
Requires:         libxml2
Requires:         libjpeg-turbo
Requires:         zlib
Requires:         libtiff
Requires:         freetype
Requires:         libmemcached
Conflicts:        geonode
AutoReqProv:      no

%description
Boundless Exchange is a web-based platform for your content, built for your enterprise.
It facilitates the creation, sharing, and collaborative use of geospatial data.
For power users, advanced editing capabilities for versioned workflows via the web browser are included.
Boundless Exchange is powered by GeoNode, GeoGig and GeoServer.

%prep

%build

%install
# create directory structure
EXCHANGE_LIB=$RPM_BUILD_ROOT/opt/boundless/%{name}
mkdir -p $EXCHANGE_LIB/{.storage,bex}/{static,media/thumbs}
touch $EXCHANGE_LIB/bex/__init__.py

# create virtualenv install geonode-exchange and python dependencies
pushd $EXCHANGE_LIB

%if %{?rhel} < 7
/usr/local/bin/virtualenv .venv
%else
virtualenv .venv
%endif

source /etc/profile.d/vendor-libs.sh
source .venv/bin/activate
python -m pip --version

%if %{?rhel} > 6
python -m pip install pip==8.1.2 --upgrade
%endif

# .mil adjustments
mkdir deleteme && cd deleteme
git clone -b %{branch} https://github.com/boundlessgeo/exchange.git
python -m pip install -r exchange/requirements.txt
cd .. && rm -fr deleteme

# Install requirements from specifc commit
python -m pip install git+https://github.com/boundlessgeo/exchange.git@%{branch}#egg=geonode-exchange

popd

# setup supervisord configuration
SUPV_ETC=$RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $SUPV_ETC
install -m 644 %{SOURCE0} $SUPV_ETC/supervisord.conf
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/celery

# setup init.d script
INITD=$RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $INITD
install -m 751 %{SOURCE1} $INITD/%{name}

# setup httpd configuration
HTTPD_CONFD=$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $HTTPD_CONFD
install -m 644 %{SOURCE2} $HTTPD_CONFD/%{name}.conf
install -m 644 %{SOURCE3} $HTTPD_CONFD/proxy.conf

# adjust virtualenv to /opt/boundless/exchange path
VAR0=$RPM_BUILD_ROOT/opt/boundless/%{name}
VAR1=/opt/boundless/%{name}
find $VAR0 -type f -name '*pyc' -exec rm -f {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# exchange-config command
USER_BIN=$RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $USER_BIN
install -m 755 %{SOURCE5} $USER_BIN/

# supervisor process scripts
install -m 755 %{SOURCE6} $EXCHANGE_LIB
install -m 755 %{SOURCE7} $EXCHANGE_LIB

# profile.d script
PROFILE_D=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
mkdir -p $PROFILE_D
install -m 755 %{SOURCE8} $PROFILE_D

# bex scripts
install -m 755 %{SOURCE9} $EXCHANGE_LIB
install -m 755 %{SOURCE4} $EXCHANGE_LIB/bex
install -m 755 %{SOURCE10} $EXCHANGE_LIB/bex

# exchange bash_profile
echo "source /etc/profile.d/exchange-settings.sh" > $EXCHANGE_LIB/.bash_profile
echo "source /opt/boundless/exchange/.venv/bin/activate" >> $EXCHANGE_LIB/.bash_profile

%pre
getent group geoservice >/dev/null || groupadd -r geoservice
getent passwd tomcat >/dev/null && usermod -a -G geoservice tomcat >/dev/null
getent passwd apache >/dev/null && usermod -a -G geoservice apache >/dev/null
getent passwd %{name} >/dev/null && usermod -a -G geoservice %{name} >/dev/null || useradd -r -d /opt/boundless/%{name} -g geoservice -s /bin/bash -c "Exchange Daemon User" %{name} >/dev/null
%post

%preun
find /opt/boundless/%{name} -type f -name '*pyc' -exec rm {} +
if [ $1 -eq 0 ] ; then
  if [[ ! -z $(ps -ef | grep tomcat8) ]] ; then
    /sbin/service tomcat8 stop > /dev/null 2>&1
    /sbin/service %{name} stop > /dev/null 2>&1
  fi
  if [[ ! -z $(ps -ef | grep httpd) ]] ; then
    /sbin/service httpd stop > /dev/null 2>&1
  fi
  /sbin/chkconfig --del %{name}
fi

%postun

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,%{name},geoservice,755)
/opt/boundless/%{name}
%defattr(755,%{name},geoservice,755)
/opt/boundless/%{name}/.venv/bin
/opt/boundless/%{name}/*.sh
/opt/boundless/%{name}/*.py
%defattr(644,%{name},geoservice,755)
%dir /opt/boundless/%{name}/.storage/static
%dir /opt/boundless/%{name}/.storage/media
%defattr(644,%{name},geoservice,755)
%dir %{_localstatedir}/log/celery
%dir %{_localstatedir}/log/%{name}
%defattr(644,apache,apache,755)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%config %{_sysconfdir}/init.d/%{name}
%{_prefix}/bin/%{name}-config
%{_sysconfdir}/profile.d/%{name}-settings.sh
%doc ../SOURCES/license/GPLv3

%changelog
* Wed Feb 01 2017 Daniel Berry <dberry@boundlessgeo.com> [1.2.0rc1-2]
- Removed rabbitmq requirement and adjustments to pre and preun
* Tue Jan 24 2017 Daniel Berry <dberry@boundlessgeo.com> [1.2.0rc1-1]
- Added boundless-vendor-libs requirement
* Thu Nov 10 2016 BerryDaniel <dberry@boundlessgeo.com> [1.1.0rc1-2]
- adjusted the exchange-config to support el7 firewalld
* Fri Oct 28 2016 BerryDaniel <dberry@boundlessgeo.com> [1.1.0rc1-1]
- update for exchange 1.1.0rc1
- refactored rpmbuild to use exchange package instead of git repo
* Mon Sep 12 2016 mfairburn <mfairburn@boundlessgeo.com> [1.0.2]
- Updated to 1.0.2
* Wed Aug 31 2016 amirahav <arahav@boundlessgeo.com> [1.0.1-2]
- Update to 1.0.1-2
* Mon Aug 29 2016 amirahav <arahav@boundlessgeo.com> [1.0.1-1]
- Update to 1.0.1
* Sat Jul 30 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-7]
- Update local_settings.py symlink
* Thu Jul 28 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-6]
- update for exchange 1.0 Final
* Thu Jul 21 2016 BerryDaniel <dberry@boundlessgeo.com> [1.0.0-5]
- update for exchange rc5
* Sat Apr 30 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-3]
- Allow remote services for all users
- workaround for get_legend errors
* Fri Apr 22 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-2]
- Use databaseSecurityClient by default
* Thu Apr 21 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-rc1]
- Remove .git directories
* Tue Apr 19 2016 BerryDaniel <dberry@boundlessgeo.com> [1.0.0-0.1rc]
- Initial RPM for Boundless Exchange
