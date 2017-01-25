Summary: Relay for bidirectional data transfer between 2 channels
Name: socat
Version: 1.7.2.4
Release: 1%{?dist}
License: GPL
Group: Applications/Internet
URL: http://www.dest-unreach.org/socat/

Source: http://www.dest-unreach.org/socat/download/socat-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
BuildRequires: readline-devel, openssl-devel
Requires: tcp_wrappers

%description
socat is a relay for bidirectional data transfer between two independent data
channels. Each of these data channels may be a file, pipe, device (serial line
etc. or a pseudo terminal), a socket (UNIX, IP4, IP6 - raw, UDP, TCP), an
SSL socket, proxy CONNECT connection, a file descriptor (stdin etc.), the GNU
line editor, a program, or a combination of two of these.

%prep
%setup

%build
%configure --disable-fips
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc BUGREPORTS CHANGES COPYING* DEVELOPMENT EXAMPLES FAQ FILES PORTING README SECURITY
%doc *.sh doc/*.css doc/*.help doc/*.html
%doc %{_mandir}/man1/socat.1*
%{_bindir}/filan
%{_bindir}/procan
%{_bindir}/socat

%changelog
* Tue Jan 09 2017 Daniel Berry <dberry@boundlessgeo.com> - 1.7.2.4-1
- Updated to release 1.7.2.4.
