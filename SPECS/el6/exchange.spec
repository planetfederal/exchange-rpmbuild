# Define Constants
%define name exchange
%define version 1.0.0
%define release 6%{?dist}
%define git_link %{git_url}
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:             %{name}
Version:          %{version}
Release:          %{release}
Summary:          Boundless Exchange, Web GIS for Everyone
Group:            Applications/Engineering
License:          GPLv2
Packager:         BerryDaniel <dberry@boundlessgeo.com>
Source0:          supervisord.conf
Source1:          %{name}.init
Source2:          %{name}-el6.conf
Source3:          proxy-el6.conf
Source4:          local_settings.py
Source5:          %{name}-config
Source6:          celery-worker.sh
Source7:          waitress.sh
Source8:          %{name}-settings.sh
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    python27-devel
BuildRequires:    python27-virtualenv
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    make
BuildRequires:    expat-devel
BuildRequires:    db4-devel
BuildRequires:    gdbm-devel
BuildRequires:    sqlite-devel
BuildRequires:    readline-devel
BuildRequires:    zlib-devel
BuildRequires:    bzip2-devel
BuildRequires:    openssl-devel
BuildRequires:    openldap-devel
BuildRequires:    tk-devel
BuildRequires:    gdal-devel >= 2.0.1
BuildRequires:    libxslt-devel
BuildRequires:    libxml2-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    zlib-devel
BuildRequires:    libtiff-devel
BuildRequires:    freetype-devel
BuildRequires:    lcms2-devel
BuildRequires:    proj-devel
BuildRequires:    geos-devel
BuildRequires:    postgresql95-devel
BuildRequires:    unzip
BuildRequires:    git
Requires:         python27
Requires:         python27-virtualenv
Requires:         gdal >= 2.0.1
Requires:         httpd
Requires:         mod_ssl
Requires:         openldap
Requires:         libxslt
Requires:         libxml2
Requires:         libjpeg-turbo
Requires:         zlib
Requires:         libtiff
Requires:         freetype
Requires:         lcms2
Requires:         proj
Requires:         geos
Requires:         rabbitmq-server >= 3.5.6
Requires:         erlang >= 18.1
Requires:         mod_xsendfile
AutoReqProv:      no

%description
Boundless Exchange is a web-based platform for your content, built for your enterprise.
It facilitates the creation, sharing, and collaborative use of geospatial data.
For power users, advanced editing capabilities for versioned workflows via the web browser are included.
Boundless Exchange is powered by GeoNode, GeoGig and Boundless Suite.

%prep

%build

%install
# exchange module
BOUNDLESS_LIB=$RPM_BUILD_ROOT/opt/boundless
mkdir -p $BOUNDLESS_LIB
pushd $BOUNDLESS_LIB
git clone %{git_link}
popd
EXCHANGE_LIB=$BOUNDLESS_LIB/%{name}
pushd $EXCHANGE_LIB
# add docs
git submodule update --init
mkdir -p $EXCHANGE_LIB/.storage/{static,media/thumbs}
# Make sure we don't package .git or dev directories
rm -rf $EXCHANGE_LIB/{.git,dev}

# create virtualenv install python dependencies
virtualenv .venv
export PATH=/usr/pgsql-9.5/bin:$PATH
source .venv/bin/activate
pip install -r requirements.txt
popd

# Make sure we don't package .git
rm -rf $EXCHANGE_LIB/.venv/src/{geonode,django-maploom,django-geoexplorer}/.git

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
find $VAR0 -type f -name '*pyc' -exec rm {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# setup exchange configuration directory
EXCHANGE_CONF=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $EXCHANGE_CONF
# local_settings.py
install -m 775 %{SOURCE4} $EXCHANGE_CONF/local_settings.py

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

%pre
getent group geoservice >/dev/null || groupadd -r geoservice
usermod -a -G geoservice tomcat
usermod -a -G geoservice apache
getent passwd %{name} >/dev/null || useradd -r -d /opt/boundless/%{name} -g geoservice -s /bin/bash -c "Exchange Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  ln -s %{_sysconfdir}/%{name}/local_settings.py /opt/boundless/%{name}/%{name}/local_settings.py
  if [ -d /opt/boundless/%{name}/geoserver_data ]; then
    chgrp -hR geoservice /opt/boundless/%{name}/geoserver_data
    chmod -R 775 /opt/boundless/%{name}/geoserver_data
  fi
fi

%preun
find /opt/boundless/%{name} -type f -name '*pyc' -exec rm {} +
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat8 stop > /dev/null 2>&1
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/service httpd stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
  # backup geoserver data dir
  mkdir -p /opt/boundless/%{name}.rpmsave
  mv /opt/boundless/%{name}/geoserver_data /opt/boundless/%{name}.rpmsave
  rm -fr /opt/boundless/%{name}
fi

%postun

%clean
#[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,%{name},geoservice,755)
/opt/boundless/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/local_settings.py
%defattr(775,%{name},geoservice,775)
%dir /opt/boundless/%{name}/.storage/static
%dir /opt/boundless/%{name}/.storage/media
%defattr(744,%{name},geoservice,744)
%dir %{_localstatedir}/log/celery
%dir %{_localstatedir}/log/%{name}
%defattr(644,%{name},geoservice,644)
%dir %{_sysconfdir}/%{name}/
%defattr(644,apache,apache,644)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/supervisord.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}
%{_prefix}/bin/%{name}-config
%{_sysconfdir}/profile.d/%{name}-settings.sh
%doc ../SOURCES/license/GNU

%changelog
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
