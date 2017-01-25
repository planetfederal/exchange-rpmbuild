# Copyright Pivotal Software, Inc. 2012-2015. All Rights Reserved.
#
# The contents of this file are subject to the Erlang Public License,
# Version 1.1, (the "License"); you may not use this file except in
# compliance with the License. You should have received a copy of the
# Erlang Public License along with this software. If not, it can be
# retrieved online at http://www.erlang.org/.
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and limitations
# under the License.

%global upstream_ver 18.3.4.4

%define OSL_File_Name Erlang_ASL2_LICENSE.txt
%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Name:		erlang
Version:	%{upstream_ver}
Release:	1%{?dist}
Summary:	General-purpose programming language and runtime environment

Group:		Development/Languages
License:	ERPL
URL:		  https://github.com/erlang/otp
Source0:	https://github.com/erlang/otp/archive/OTP-%{upstream_ver}.tar.gz
Source2:  %{OSL_File_Name}
Vendor:		Pivotal Software, Inc.


#   Do not format man-pages and do not install miscellaneous
Patch1: otp-0001-Do-not-format-man-pages-and-do-not-install-miscellan.patch
#   Remove rpath
Patch2: otp-0002-Remove-rpath.patch
#   Do not install C sources
Patch3: otp-0003-Do-not-install-C-sources.patch
#   Do not install erlang sources
Patch7: otp-0007-Do-not-install-erlang-sources.patch


# BuildRoot not strictly needed since F10, but keep it for spec file robustness
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	m4

Obsoletes: erlang-docbuilder
Provides: erlang

%description
This is a minimal packaging of Erlang produced by Pivotal to support
running RabbitMQ. Compared to the community Erlang packaging it is
monolithic, has fewer dependencies, and has lower disk and memory
overhead. Many applications from Erlang Open Telecom Platform (OTP)
have been removed. The following applications remain: asn1, compiler,
crypto, erl_interface, erts, hipe, inets, kernel, mnesia, os_mon,
otp_mibs, public_key, reltool, runtime_tools, sasl, snmp, ssl, stdlib,
syntax_tools and xmerl.

%define _pivotal_license_file %{_builddir}/otp-OTP-%{upstream_ver}/`basename %{S:2}`


%prep
%setup -q -n otp-OTP-%{upstream_ver}

%patch1 -p1 -b .Do_not_format_man_pages_and_do_not_install_miscellan
%patch2 -p1 -b .Remove_rpath
%patch3 -p1 -b .Do_not_install_C_sources
%patch7 -p1 -b .Do_not_install_erlang_sources

# remove shipped zlib sources
# commented out because centos only has 1.2.3 and Erlang 18.1 needs a later version
#rm -f erts/emulator/zlib/*.[ch]


# Fix 664 file mode
chmod 644 lib/kernel/examples/uds_dist/c_src/Makefile
chmod 644 lib/kernel/examples/uds_dist/src/Makefile
chmod 644 lib/ssl/examples/certs/Makefile
chmod 644 lib/ssl/examples/src/Makefile


%build
%global conf_flags --enable-shared-zlib --without-javac --without-odbc


# autoconf
./otp_build autoconf

%ifarch sparcv9 sparc64
CFLAGS="$RPM_OPT_FLAGS -mcpu=ultrasparc -fno-strict-aliasing" %configure %{conf_flags}
%else
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %configure %{conf_flags}
%endif


# remove pre-built stuff
make clean

cp %{S:2} %{_pivotal_license_file}

touch lib/common_test/SKIP
touch lib/cosEvent/SKIP
touch lib/cosEventDomain/SKIP
touch lib/cosFileTransfer/SKIP
touch lib/cosNotification/SKIP
touch lib/cosProperty/SKIP
touch lib/cosTime/SKIP
touch lib/cosTransactions/SKIP
touch lib/debugger/SKIP
touch lib/dialyzer/SKIP
touch lib/diameter/SKIP
touch lib/edoc/SKIP
touch lib/et/SKIP
touch lib/erl_docgen/SKIP
touch lib/gs/SKIP
touch lib/ic/SKIP
touch lib/jinterface/SKIP
touch lib/megaco/SKIP
touch lib/observer/SKIP
touch lib/odbc/SKIP
touch lib/orber/SKIP
touch lib/ose/SKIP
touch lib/percept/SKIP
touch lib/ssh/SKIP
touch lib/test_server/SKIP
touch lib/typer/SKIP
touch lib/webtool/SKIP
touch lib/wx/SKIP

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Do not install info files - they are almost empty and useless
find $RPM_BUILD_ROOT%{_libdir}/erlang -type f -name info -exec rm -f {} \;

# fix 0775 permission on some directories
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/erlang/bin

# Win32-specific man-pages
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/man/man1/erlsrv.*
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/man/man1/werl.*
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/man/man3/win32reg.*

# remove empty directory
rm -r $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/man

# remove outdated script
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/Install

# Replace identical executables with symlinks
for exe in $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/bin/*
do
	base="$(basename "$exe")"
	next="$RPM_BUILD_ROOT%{_libdir}/erlang/bin/${base}"
	rel="$(echo "$exe" | sed "s,^$RPM_BUILD_ROOT%{_libdir}/erlang/,../,")"
	if cmp "$exe" "$next"; then
		ln -sf "$rel" "$next"
	fi
done
for exe in $RPM_BUILD_ROOT%{_libdir}/erlang/bin/*
do
	base="$(basename "$exe")"
	next="$RPM_BUILD_ROOT%{_bindir}/${base}"
	rel="$(echo "$exe" | sed "s,^$RPM_BUILD_ROOT,,")"
	if cmp "$exe" "$next"; then
		ln -sf "$rel" "$next"
	fi
done

rm -rf $RPM_BUILD_ROOT%{_bindir}/ct_run
rm -rf $RPM_BUILD_ROOT%{_bindir}/dialyzer
rm -rf $RPM_BUILD_ROOT%{_bindir}/run_test
rm -rf $RPM_BUILD_ROOT%{_bindir}/typer
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/bin/ct_run
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/bin/dialyzer
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/bin/run_test
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/bin/typer
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/bin/ct_run
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/bin/dialyzer
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/bin/typer
rm -rf $RPM_BUILD_ROOT%{_libdir}/erlang/lib/*/examples

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)

%doc %{OSL_File_Name}

%dir %{_libdir}/erlang/lib/asn1-*/
%{_libdir}/erlang/lib/asn1-*/ebin
%{_libdir}/erlang/lib/asn1-*/priv
%{_libdir}/erlang/lib/asn1-*/src


%{_libdir}/erlang/lib/compiler-*/


%{_libdir}/erlang/lib/crypto-*/

%dir %{_libdir}/erlang/lib/eldap-*/
%{_libdir}/erlang/lib/eldap-*/asn1
%{_libdir}/erlang/lib/eldap-*/ebin
%{_libdir}/erlang/lib/eldap-*/include
%{_libdir}/erlang/lib/eldap-*/src

%{_libdir}/erlang/lib/eunit-*/

%{_libdir}/erlang/lib/erl_interface-*/


%dir %{_libdir}/erlang/
%dir %{_libdir}/erlang/bin/
%dir %{_libdir}/erlang/lib/
%dir %{_libdir}/erlang/releases/
%{_bindir}/epmd
%{_bindir}/erl
%{_bindir}/erlc
%{_bindir}/escript
%{_bindir}/run_erl
%{_bindir}/to_erl
%{_libdir}/erlang/bin/epmd
%{_libdir}/erlang/bin/erl
%{_libdir}/erlang/bin/erlc
%{_libdir}/erlang/bin/escript
%{_libdir}/erlang/bin/no_dot_erlang.boot
%{_libdir}/erlang/bin/run_erl
%{_libdir}/erlang/bin/start
%{_libdir}/erlang/bin/start.boot
%{_libdir}/erlang/bin/start.script
%{_libdir}/erlang/bin/start_clean.boot
%{_libdir}/erlang/bin/start_erl
%{_libdir}/erlang/bin/start_sasl.boot
%{_libdir}/erlang/bin/to_erl
%dir %{_libdir}/erlang/erts-*/bin
%{_libdir}/erlang/erts-*/bin/beam
%{_libdir}/erlang/erts-*/bin/beam.smp
%{_libdir}/erlang/erts-*/bin/child_setup
%{_libdir}/erlang/erts-*/bin/dyn_erl
%{_libdir}/erlang/erts-*/bin/epmd
%{_libdir}/erlang/erts-*/bin/erl
%{_libdir}/erlang/erts-*/bin/erl.src
%{_libdir}/erlang/erts-*/bin/erlc
%{_libdir}/erlang/erts-*/bin/erlexec
%{_libdir}/erlang/erts-*/bin/escript
%{_libdir}/erlang/erts-*/bin/heart
%{_libdir}/erlang/erts-*/bin/inet_gethost
%{_libdir}/erlang/erts-*/bin/run_erl
%{_libdir}/erlang/erts-*/bin/start
%{_libdir}/erlang/erts-*/bin/start.src
%{_libdir}/erlang/erts-*/bin/start_erl.src
%{_libdir}/erlang/erts-*/bin/to_erl
%{_libdir}/erlang/erts-*/include
%{_libdir}/erlang/erts-*/lib
%{_libdir}/erlang/erts-*/src
%{_libdir}/erlang/lib/erts-*/
%{_libdir}/erlang/releases/*
%{_libdir}/erlang/usr/


%{_libdir}/erlang/lib/hipe-*/


%dir %{_libdir}/erlang/lib/inets-*/
%{_libdir}/erlang/lib/inets-*/ebin
%{_libdir}/erlang/lib/inets-*/include
%{_libdir}/erlang/lib/inets-*/priv
%{_libdir}/erlang/lib/inets-*/src


%dir %{_libdir}/erlang/lib/kernel-*/
%{_libdir}/erlang/lib/kernel-*/ebin
%{_libdir}/erlang/lib/kernel-*/include
%{_libdir}/erlang/lib/kernel-*/src


%dir %{_libdir}/erlang/lib/mnesia-*/
%{_libdir}/erlang/lib/mnesia-*/ebin
%{_libdir}/erlang/lib/mnesia-*/include
%{_libdir}/erlang/lib/mnesia-*/src


%{_libdir}/erlang/lib/os_mon-*/

%{_libdir}/erlang/lib/otp_mibs-*/

%{_libdir}/erlang/lib/parsetools-*/

%{_libdir}/erlang/lib/public_key-*/


%dir %{_libdir}/erlang/lib/reltool-*/
%{_libdir}/erlang/lib/reltool-*/ebin
%{_libdir}/erlang/lib/reltool-*/src

%dir %{_libdir}/erlang/lib/syntax_tools-*/
%{_libdir}/erlang/lib/syntax_tools-*/ebin
%{_libdir}/erlang/lib/syntax_tools-*/include

%{_libdir}/erlang/lib/runtime_tools-*/


%dir %{_libdir}/erlang/lib/sasl-*/
%{_libdir}/erlang/lib/sasl-*/ebin
%{_libdir}/erlang/lib/sasl-*/src


%dir %{_libdir}/erlang/lib/snmp-*/
%{_libdir}/erlang/lib/snmp-*/bin
%{_libdir}/erlang/lib/snmp-*/ebin
%{_libdir}/erlang/lib/snmp-*/include
%{_libdir}/erlang/lib/snmp-*/mibs
%{_libdir}/erlang/lib/snmp-*/priv
%{_libdir}/erlang/lib/snmp-*/src


%dir %{_libdir}/erlang/lib/ssl-*/
%{_libdir}/erlang/lib/ssl-*/ebin
%{_libdir}/erlang/lib/ssl-*/src


%dir %{_libdir}/erlang/lib/stdlib-*/
%{_libdir}/erlang/lib/stdlib-*/ebin
%{_libdir}/erlang/lib/stdlib-*/include
%{_libdir}/erlang/lib/stdlib-*/src


%dir %{_libdir}/erlang/lib/syntax_tools-*/
%{_libdir}/erlang/lib/syntax_tools-*/ebin

%{_libdir}/erlang/lib/tools-*/

%{_libdir}/erlang/lib/xmerl-*/


%changelog
* Thu Nov 03 2016 BerryDaniel <dberry@boundlessgeo.com> [18.3.4.4-1]
- Updated to 18.3.4.4
