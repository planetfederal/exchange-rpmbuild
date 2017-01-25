%define __jar_repack %{nil}
%define tomcat_home /usr/share/tomcat8
%define tomcat_group tomcat
%define tomcat_user tomcat
%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Summary:    Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Name:       tomcat8
Version:    8.5.9
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Source1:    %{name}.init
Source2:    %{name}.sysconfig
Source3:    %{name}.logrotate
Requires:   java
Conflicts:   tomcat
#BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on Sun's JDK and not
on JPP packages.

%package admin-webapps
Group: System Environment/Applications
Summary: The host-manager and manager web applications for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description admin-webapps
The host-manager and manager web applications for Apache Tomcat.

%package docs-webapp
Group: System Environment/Applications
Summary: The docs web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description docs-webapp
The docs web application for Apache Tomcat.

%package examples-webapp
Group: System Environment/Applications
Summary: The examples web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description examples-webapp
The examples web application for Apache Tomcat.

%package root-webapp
Group: System Environment/Applications
Summary: The ROOT web application for Apache Tomcat
Requires: %{name} = %{version}-%{release}

%description root-webapp
The ROOT web application for Apache Tomcat.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/%{name}/
cd %{buildroot}/%{tomcat_home}/
ln -s /var/log/%{name}/ logs
cd -

# Put temp in /var/cache and link back.
rm -rf %{buildroot}/%{tomcat_home}/temp
install -d -m 755 %{buildroot}/var/cache/%{name}/temp
cd %{buildroot}/%{tomcat_home}/
ln -s /var/cache/%{name}/temp temp
cd -

# Put work in /var/cache and link back.
rm -rf %{buildroot}/%{tomcat_home}/work
install -d -m 755 %{buildroot}/var/cache/%{name}/work
cd %{buildroot}/%{tomcat_home}/
ln -s /var/cache/%{name}/work work
cd -

# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{_sysconfdir}/%{name}/Catalina/localhost
install -m 644 %_sourcedir/context.xml %{buildroot}/%{tomcat_home}/conf/context.xml
mv %{buildroot}/%{tomcat_home}/conf/* %{buildroot}/%{_sysconfdir}/%{name}/
rmdir %{buildroot}/%{tomcat_home}/conf
cd %{buildroot}/%{tomcat_home}/
ln -s %{_sysconfdir}/%{name} conf
cd -

# Put webapps in /var/lib and link back.
install -d -m 755 %{buildroot}/var/lib/%{name}
mv %{buildroot}/%{tomcat_home}/webapps %{buildroot}/var/lib/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s /var/lib/%{name}/webapps webapps
cd -

# Put lib in /usr/share/java and link back.
install -d -m 755 %{buildroot}/usr/share/java
mv %{buildroot}/%{tomcat_home}/lib %{buildroot}/usr/share/java/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s /usr/share/java/%{name} lib
cd -

# Put docs in /usr/share/doc
install -d -m 755 %{buildroot}/usr/share/doc/%{name}-%{version}
mv %{buildroot}/%{tomcat_home}/{RUNNING.txt,LICENSE,NOTICE,RELEASE*} %{buildroot}/usr/share/doc/%{name}-%{version}

# Put executables in /usr/bin
rm  %{buildroot}/%{tomcat_home}/bin/*bat
install -d -m 755 %{buildroot}/usr/{bin,sbin}
mv %{buildroot}/%{tomcat_home}/bin/digest.sh %{buildroot}/usr/bin/%{name}-digest
mv %{buildroot}/%{tomcat_home}/bin/tool-wrapper.sh %{buildroot}/usr/bin/%{name}-tool-wrapper

%if 0%{?rhel} == 6
# Drop init script
install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{name}.init %{buildroot}/%{_initrddir}/%{name}

# Drop sysconfig script
install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%else if 0%{?rhel} == 7
install -d -m 755 %{buildroot}/%{_sysconfdir}/systemd/system
install -m 644 %_sourcedir/%{name}.service %{buildroot}/%{_sysconfdir}/systemd/system/%{name}.service
%endif

# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
/var/log/%{name}/
/var/cache/%{name}
%dir /var/lib/%{name}/webapps
%defattr(-,root,root)
%{tomcat_home}/*
%attr(0755,root,root) /usr/bin/*
%dir /var/lib/%{name}

%if 0%{?rhel} == 6
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%else if 0%{?rhel} == 7
%{_sysconfdir}/systemd/system/%{name}.service
%endif

%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%doc /usr/share/doc/%{name}-%{version}
%defattr(0644,root,root,0755)
/usr/share/java/%{name}

%files admin-webapps
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/host-manager
/var/lib/%{name}/webapps/manager

%files docs-webapp
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/docs

%files examples-webapp
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/examples

%files root-webapp
%defattr(0644,root,root,0755)
/var/lib/%{name}/webapps/ROOT

%post
%if 0%{?rhel} == 6
chkconfig --add %{name}
%else if 0%{?rhel} == 7
systemctl daemon-reload
%endif

%preun
if [ $1 = 0 ]; then
  %if 0%{?rhel} == 6
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
  %else if 0%{?rhel} == 7
  systemctl stop %{name} > /dev/null 2>&1
  %endif
fi

%postun
if [ $1 -ge 1 ]; then
  %if 0%{?rhel} == 6
  service %{name} condrestart > /dev/null 2>&1
  %else if 0%{?rhel} == 7
  systemctl condrestart %{name} > /dev/null 2>&1
  %endif
fi

%changelog
* Sat Nov 12 2016 amirahav <arahav@boundlessgeo.com> [8.5.8-1]
- Bump to 8.5.8
* Thu Nov 03 2016 BerryDaniel <dberry@boundlessgeo.com> [8.5.6-1]
- Updated to 8.5.6
