# Define Constants
%define name registry
%define _version 0.0.1
%define _release 2
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
Summary:          Registry is a web-based platform that captures geo-spatial content using CSW-T protocol.
Group:            Applications/Engineering
License:          MIT
Packager:         BerryDaniel <dberry@boundlessgeo.com>
Source0:          supv_%{name}.conf
Source1:          %{name}.init
%{?el6:Source2:   httpd-proxy-el6.conf}
%{?el7:Source2:   httpd-proxy-el7.conf}
Source3:          %{name}-settings.sh
Source4:          %{name}-createdb
Source5:          %{name}.sh
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
BuildRequires:    freetype-devel
BuildRequires:    gcc
BuildRequires:    git
BuildRequires:    libxml2-devel
BuildRequires:    libxslt-devel
BuildRequires:    sqlite-devel
BuildRequires:    wget
BuildRequires:    zlib-devel
%{?el6:Requires: python27}
%{?el6:Requires: python27-virtualenv}
%{?el7:Requires: python}
%{?el7:Requires: python-virtualenv}
Requires:         boundless-vendor-libs
Requires:         freetype
Requires:         libxml2
Requires:         libxslt
Requires:         zlib
AutoReqProv:      no

%description
Registry is a web-based platform that captures geo-spatial content using CSW-T
protocol. Information is indexed into the Elasticsearch engine allowing fast
searches.

%prep

%build

%install
# create directory structure
REGISTRY_ROOT=$RPM_BUILD_ROOT/opt/%{name}
mkdir -p $REGISTRY_ROOT

# create virtualenv install dependencies
pushd $REGISTRY_ROOT

%if %{?rhel} < 7
/usr/local/bin/virtualenv .venv
%else
virtualenv .venv
%endif

source /etc/profile.d/vendor-libs.sh
source .venv/bin/activate

%if %{?rhel} > 6
python -m pip install pip==8.1.2 --upgrade
%endif

# .mil adjustments
mkdir deleteme && cd deleteme
git clone -b %{branch} https://github.com/boundlessgeo/registry.git
python -m pip install -r registry/requirements.txt
cp registry/registry.py ..
cp registry/documentation.md ..
cd .. && rm -fr deleteme

# Install additional dependencies
python -m pip install psycopg2==2.6.1 supervisor==3.3.1 Pillow==3.4.2


# modify location in registry.py, so documentation displays at the endpoint
sed -i 's@documentation.md@/opt/registry/documentation.md@g' registry.py

# modify documentation.md to reflect new port (8001)
sed -i 's@localhost:8000@localhost:8001@g' registry.py

popd

# install supervisor configuration
install -m 644 %{SOURCE0} $REGISTRY_ROOT/supv_registry.conf

# install init.d script
INITD=$RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $INITD
install -m 751 %{SOURCE1} $INITD/%{name}

# install httpd proxy configuration
HTTPD_CONFD=$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $HTTPD_CONFD
install -m 644 %{SOURCE2} $HTTPD_CONFD/_%{name}-proxy.conf

# adjust virtualenv to /opt/registry path
VAR0=$RPM_BUILD_ROOT/opt/%{name}
VAR1=/opt/%{name}
find $VAR0 -type f -name '*pyc' -exec rm -f {} +
grep -rl $VAR0 $VAR0 | xargs sed -i 's|'$VAR0'|'$VAR1'|g'

# profile.d script
PROFILE_D=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
mkdir -p $PROFILE_D
install -m 755 %{SOURCE3} $PROFILE_D

# registry-creatdb command
USER_BIN=$RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $USER_BIN
install -m 755 %{SOURCE4} $USER_BIN/

# registry shell script that supervisor will run (loads profile.d settings)
install -m 755 %{SOURCE5} $REGISTRY_ROOT/

%pre
getent group geoservice >/dev/null || groupadd -r geoservice
getent passwd %{name} >/dev/null || useradd -r -d /opt/%{name} -g geoservice -s /bin/bash -c "Registry Daemon User" %{name}

%post

%preun
find /opt/%{name} -type f -name '*pyc' -exec rm {} +
if [ $1 -eq 0 ] ; then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi

%postun

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,%{name},geoservice,755)
/opt/%{name}
%defattr(755,%{name},geoservice,755)
/opt/%{name}/.venv/bin
/opt/%{name}/registry.*
%defattr(644,apache,apache,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/_%{name}-proxy.conf
%defattr(-,root,root,-)
%config %{_sysconfdir}/init.d/%{name}
%{_prefix}/bin/%{name}-createdb
%{_sysconfdir}/profile.d/%{name}-settings.sh

%changelog
* Thu Feb 2 2017 BerryDaniel <dberry@boundlessgeo.com> [0.0.1-2]
- NODE-702 (Rename registry_proxy.conf to _registry_proxy.conf)
- remove trailing slash in proxy conf file
* Thu Jan 5 2017 BerryDaniel <dberry@boundlessgeo.com> [0.0.1-1]
- Initial RPM for Registry
