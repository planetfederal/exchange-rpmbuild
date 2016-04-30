# Define Constants
%define name exchange
%define version 1.0.0
%define release 3%{?dist}
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
Source2:          %{name}-el7.conf
Source3:          proxy-el7.conf
Source4:          local_settings.py
Source5:          %{name}-config
Patch0:        base.html.patch
Patch1:        models.py.patch
Requires(pre):    /usr/sbin/useradd
Requires(pre):    /usr/bin/getent
Requires(pre):    bash
Requires(postun): /usr/sbin/userdel
Requires(postun): bash
BuildRequires:    python-devel
BuildRequires:    python-virtualenv
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
Requires:         python
Requires:         python-virtualenv
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
GEONODE_LIB=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
mkdir -p $GEONODE_LIB/django/{static,media/thumbs}
pushd $GEONODE_LIB
git clone %{git_link}
# Make sure we don't package .git or dev directories
rm -rf $GEONODE_LIB/%{name}/{.git,dev}

# create virtualenv
virtualenv .
export PATH=/usr/pgsql-9.5/bin:$PATH
source bin/activate

# install python dependencies
pushd %{name}
pip install -r requirements.txt
popd

# Make sure we don't package .git
rm -rf $GEONODE_LIB/src/{geonode,django-maploom,django-geoexplorer}/.git

# Allow remote services and workaround for get_legend
pushd $GEONODE_LIB/src/geonode
patch -p0 < %{PATCH0}
patch -p0 < %{PATCH1}
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

# adjust virtualenv to /var/lib/geonode path
VAR0=$RPM_BUILD_ROOT%{_localstatedir}/lib/geonode
VAR1=%{_localstatedir}/lib/geonode
find $VAR0 -type f -name '*pyc' -exec rm {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# setup exchange configuration directory
EXCHANGE_CONF=$RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $EXCHANGE_CONF
# local_settings.py
install -m 775 %{SOURCE4} $EXCHANGE_CONF/local_settings.py

# add robots.txt as a TemplateView in urls
printf "User-agent: *\nDisallow: /geoserver/" > $GEONODE_LIB/%{name}/%{name}/templates/robots.txt
sed -i "s|urlpatterns = patterns('',|urlpatterns = patterns('',\\n\
url(r'^/robots\\\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),|" $RPM_BUILD_ROOT%{_localstatedir}/lib/geonode/%{name}/%{name}/urls.py

# exchange-config command
USER_BIN=$RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $USER_BIN
install -m 755 %{SOURCE5} $USER_BIN/

%pre
getent group geoservice >/dev/null || groupadd -r geoservice
usermod -a -G geoservice tomcat
usermod -a -G geoservice apache
getent passwd %{name} >/dev/null || useradd -r -d %{_localstatedir}/lib/geonode/exchange -g geoservice -s /bin/bash -c "Exchange Daemon User" %{name}

%post
if [ $1 -eq 1 ] ; then
  ln -s %{_sysconfdir}/%{name}/local_settings.py %{_localstatedir}/lib/geonode/exchange/%{name}/local_settings.py
  if [ -d /var/lib/geoserver_data ]; then
    chgrp -hR geoservice /var/lib/geoserver_data
    chmod -R 775 /var/lib/geoserver_data
  fi
fi

%preun
find %{_localstatedir}/lib/geonode -type f -name '*pyc' -exec rm {} +
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat8 stop > /dev/null 2>&1
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/service httpd stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
      #remove soft link and virtual environment
  rm -fr %{_localstatedir}/lib/geonode
fi

%postun

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,%{name},geoservice,755)
%{_localstatedir}/lib/geonode
%config(noreplace) %{_sysconfdir}/%{name}/local_settings.py
%defattr(775,%{name},geoservice,775)
%dir %{_localstatedir}/lib/geonode/django/static
%dir %{_localstatedir}/lib/geonode/django/media
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
%doc ../SOURCES/license/GNU

%changelog
* Sat Apr 30 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-3]
- Allow remote services for all users
- workaround for get_legend errors
* Fri Apr 22 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-2]
- Use databaseSecurityClient by default
* Thu Apr 21 2016 amirahav <arahav@boundlessgeo.com> [1.0.0-rc1]
- Remove .git directories
* Tue Apr 19 2016 BerryDaniel <dberry@boundlessgeo.com> [1.0.0-0.1rc]
- Initial RPM for Boundless Exchange
