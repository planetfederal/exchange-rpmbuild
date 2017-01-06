#!/usr/bin/env bash

curl -o /etc/yum.repos.d/exchange.repo https://yum.boundlessps.com/geoshape.repo
sudo yum -y update
version=`rpm -qa \*-release | grep -Ei "redhat|centos" | cut -d"-" -f3`
if [ $version == 7 ];then
    sudo yum -y install http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-8.noarch.rpm
    sudo yum -y install python-devel python-virtualenv
else
    sudo yum -y install http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
    sudo yum -y install python27-devel python27-virtualenv
fi
sudo yum -y install gcc \
                    gcc-c++ \
                    make \
                    expat-devel \
                    db4-devel \
                    gdbm-devel \
                    sqlite-devel \
                    readline-devel \
                    zlib-devel \
                    bzip2-devel \
                    openssl-devel \
                    openldap-devel \
                    tk-devel \
                    gdal-devel >= 2.0.1 \
                    libxslt-devel \
                    libxml2-devel \
                    libjpeg-turbo-devel \
                    zlib-devel \
                    libtiff-devel \
                    freetype-devel \
                    lcms2-devel \
                    proj-devel \
                    geos-devel \
                    postgresql95-devel \
                    unzip \
                    git \
                    rpmdevtools \
                    createrepo \
                    libmemcached-devel
sudo su - vagrant
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' \
                                      --define '_sourcedir /vagrant/SOURCES/exchange' \
                                      -bb /vagrant/SPECS/exchange.spec

QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' \
                                      --define '_sourcedir /vagrant/SOURCES/geonode-geoserver' \
                                      -bb /vagrant/SPECS/geonode-geoserver.spec
