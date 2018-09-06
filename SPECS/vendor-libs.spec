%define __prefix /opt/boundless/vendor
%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%define __url https://s3.amazonaws.com/boundless-packaging/whitelisted/vendor/vendor-%{version}-%{__dist}-%{_arch}.tar.gz
%define _release 3

%if %{?rel:1}0
%define release %{rel}
%else
%define release %{_release}
%endif

%if %{?rhel} > 6
%define __dist el7
%else
%define __dist el6
%endif

Name: boundless-vendor-libs
Version:        1.2.1
Release:        %{release}%{?dist}
Summary:        Boundless vendor install containing Libraries and Headers
URL:            https://boundlessgeo.com/
Packager:       Daniel Berry <dberry@boundlessgeo.com>
License:        GPLv2
Group:          Applications/Engineering
Source0:        vendor-libs.sh
BuildRequires:  bzip2
Requires:       curl
Requires:       expat
Requires:       freetype
Requires:       libjpeg-turbo
Requires:       libtiff
Requires:       libxml2
Requires:       libxslt
Requires:       openldap
Requires:       poppler
Requires:       sqlite
Requires:       xerces-c
Requires:       zlib

%description
Boundless vendor install containing Libraries and Headers for postgresql-devel,
libkml-devel, lcms2-devel, openjpeg2-devel, geos-devel, proj-devel, swig,
and gdal.

%prep
%build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
profile_d=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
ld_so_conf_d=$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
vendor=$RPM_BUILD_ROOT/opt/boundless/vendor
mkdir -p $profile_d $ld_so_conf_d $vendor
cd $vendor
curl -o download.tar.gz %{__url}
tar -xvf download.tar.gz && rm -f download.tar.gz
install -m 755 %{SOURCE0} $profile_d/vendor-libs.sh
echo "/opt/boundless/vendor/lib" > $ld_so_conf_d/vendor.conf

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(755,root,root,755)
/opt/boundless/vendor
%{_sysconfdir}/profile.d/vendor-libs.sh
%{_sysconfdir}//ld.so.conf.d/vendor.conf

%changelog
* Thu May 4 2017 Daniel Berry <dberry@boundlessgeo.com> [1.2.0-3]
- Removed the dependency of minizip
* Wed Jan 18 2017 Daniel Berry <dberry@boundlessgeo.com> [1.2.0-1]
- First Build for Boundless Vendor Libraries
