# Define Constants
%define name exchange-development-repo
%define version 1.0.0
%define release 1
%define _unpackaged_files_terminate_build 0
%define __os_install_post %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}.%%{ARCH}.rpm

Name: %{name}
Version: %{version}
Release: %{release}
License: GPLv2
Summary: Exchange Development Repository Configuration Files
Packager: Daniel Berry <dberry@boundlessgeo.com>
Group: System Environment/Base
URL: https://exchange-development-yum.s3.amazonaws.com
Source0: exchange-development.repo
Source1: exchange-gpg-key
Source2: postgresql-gpg-key
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
This package installs the 'exchange-development.repo' repository file along
with the required gpg keys for exchange and postgresql.

%prep
%setup -c -T

%build

%install
rm -rf %{buildroot}
# repo file
install -Dpm 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/exchange-development.repo

%post
echo "     _   _   _    ";
echo "    / \ / \ / \   ";
echo "   _ B _ E _ X _  ";
echo "  / \_/ \_/ \_/ \ ";
echo " ( R _ E _ P _ O )";
echo "  \_/ \_/ \_/ \_/ ";
echo "   ( D ( E ( V )  ";
echo "    \_/ \_/ \_/   ";
echo "                  ";

%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0644)
%config %{_sysconfdir}/yum.repos.d/*

%changelog
* Wed Jan 10 2017 Daniel Berry <dberry@boundlessgeo.com> - 1.0.0-1
- Initial release 1.0.0
