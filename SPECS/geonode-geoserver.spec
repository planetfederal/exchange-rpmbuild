# Define Constants
%define name geonode-geoserver
%define realname geoserver
%define version 2.8
%define release 4
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       A version of GeoServer that is enhanced and designed for use with GeoNode.
Group:         Development/Libraries
License:       GPLv2
BuildRequires: unzip
Requires:      tomcat8
Conflicts:     geoserver
Source0:       geoserver.war
Source1:       geoserver_data-geogig_od3.zip
Source2:       geogig.config
Patch0:        web.xml.patch
Patch1:        context.xml.patch
BuildArch:     noarch

%description
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilites specifically for GeoSHAPE.

%prep
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
[ -d $RPM_SOURCE_DIR/data ] && rm -rf $RPM_SOURCE_DIR/data
unzip $RPM_SOURCE_DIR/geoserver.war -d $RPM_SOURCE_DIR/geoserver
unzip $RPM_SOURCE_DIR/geoserver_data-geogig_od3.zip -d $RPM_SOURCE_DIR/data
pushd $RPM_SOURCE_DIR/geoserver

%patch0 -p1
%patch1 -p1

popd

%build

%install
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat8/webapps
GS=$RPM_SOURCE_DIR/geoserver
DATA=$RPM_BUILD_ROOT%{_localstatedir}/lib/geoserver_data
GEOSHAPE_DATA=$RPM_SOURCE_DIR/data
mkdir -p $WEBAPPS
cp -rp $GS $WEBAPPS
if [ ! -d $DATA ]; then
  mkdir -p $DATA
  cp -R $GEOSHAPE_DATA/* $DATA
fi
#sed -i.bak "s|http://localhost|https://localhost|g" $DATA/security/auth/geonodeAuthProvider/config.xml
install -m 644 %{SOURCE2} $DATA/geogig/.geogigconfig

%pre

%post
if [ $1 -eq 1 ] ; then
  # add Java specific options
  echo '# Next line added for geonode service' >> %{_sysconfdir}/sysconfig/tomcat8
  echo 'JAVA_OPTS="-Djava.awt.headless=true -Xms256m -Xmx1024m -Xrs -XX:PerfDataSamplingInterval=500 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:SoftRefLRUPolicyMSPerMB=36000 -Duser.home=/var/lib/geoserver_data/geogig"' >> %{_sysconfdir}/sysconfig/tomcat8
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat8 stop > /dev/null 2>&1
  rm -fr %{_localstatedir}/lib/tomcat8/webapps/geoserver
fi

%postun
if [ $1 -eq 1 ] ; then
  /sbin/service tomcat8 condrestart >/dev/null 2>&1
fi

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}
[ -d $RPM_SOURCE_DIR/geoserver ] && rm -rf $RPM_SOURCE_DIR/geoserver
[ -d $RPM_SOURCE_DIR/data ] && rm -rf $RPM_SOURCE_DIR/data

%files
%defattr(-,root,root,-)
%attr(-,tomcat,tomcat) %{_localstatedir}/lib/tomcat8/webapps/geoserver
%attr(775,tomcat,tomcat) %{_localstatedir}/lib/geoserver_data
%attr(755,tomcat,tomcat) %{_localstatedir}/lib/geoserver_data/file-service-store

%changelog
%changelog
* Tue Apr 19 2016 BerryDaniel <dberry@boundlessgeo.com> [1.0.0-0.1rc]
- Initial RPM for GeoNode GeoServer
