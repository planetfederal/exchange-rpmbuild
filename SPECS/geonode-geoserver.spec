# Define Constants
%define name geonode-geoserver
%define realname geoserver
%define war_url https://yum-geonode.boundlessps.com/war/latest/geoserver.war
%define version 2.9.2
%define release 2
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       A version of GeoServer that is enhanced and designed for use with GeoNode.
Group:         Development/Libraries
License:       GPLv2
AutoReqProv: no
BuildRequires: unzip
BuildRequires: wget
Requires:      geos
Requires:      proj
Requires:      tomcat8
Conflicts:     geoserver
Conflicts:     suite-geoserver
Source0:       web.xml
Source1:       geogig.config
BuildArch:     noarch

%description
GeoServer is built with the geoserver-geonode-ext, which extends GeoServer
with certain JSON, REST, and security capabilities specifically for GeoNode.

%prep

%build

%install
WEBAPPS=$RPM_BUILD_ROOT%{_localstatedir}/lib/tomcat8/webapps
DATA=$RPM_BUILD_ROOT/opt/geonode/geoserver_data
mkdir -p $WEBAPPS
mkdir -p $DATA
wget %{war_url}
unzip geoserver.war -d $WEBAPPS/geoserver
rm -f geoserver.war
install -m 755 %{SOURCE0} $WEBAPPS/geoserver/WEB-INF/web.xml
cp -fr $WEBAPPS/geoserver/data/* $DATA

#sed -i.bak "s|http://localhost|https://localhost|g" $DATA/security/auth/geonodeAuthProvider/config.xml
mkdir -p $DATA/geogig
install -m 644 %{SOURCE1} $DATA/geogig/.geogigconfig

%pre

%post
if [ $1 -eq 1 ] ; then
  # add Java specific options
  echo '# Next line added for geonode service' >> %{_sysconfdir}/sysconfig/tomcat8
  echo 'JAVA_OPTS="-Djava.awt.headless=true -Xms256m -Xmx1536m -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:SoftRefLRUPolicyMSPerMB=36000 -Duser.home=/opt/boundless/exchange/geoserver_data/geogig"' >> %{_sysconfdir}/sysconfig/tomcat8
fi

%preun
if [ $1 -eq 0 ] ; then
  /sbin/service tomcat8 stop > /dev/null 2>&1
  rm -fr %{_localstatedir}/lib/tomcat8/webapps/geoserver
  # backup geoserver data dir
  mkdir -p /opt/geonode.rpmsave
  mv /opt/geonode/geoserver_data /opt/geonode.rpmsave
  rm -fr /opt/geonode
fi

%postun
if [ $1 -eq 1 ] ; then
  /sbin/service tomcat8 condrestart >/dev/null 2>&1
fi

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644, tomcat, tomcat, 755)
%{_localstatedir}/lib/tomcat8/webapps/geoserver
/opt/geonode/geoserver_data

%changelog
* Tue Nov 05 2016 BerryDaniel <dberry@boundlessgeo.com> [2.9.2-2]
- Upgrade to Geoserver 2.9.2
