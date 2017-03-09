#!/usr/bin/env bash

sudo yum -y update
version=`rpm -qa \*-release | grep -Ei "redhat|centos" | cut -d"-" -f3`
if [ $version == 7 ];then
    sudo yum -y install python-devel python-virtualenv
else
    sudo yum -y install python27-devel python27-virtualenv
fi
sudo yum -y install https://s3.amazonaws.com/exchange-development-yum/exchange-development-repo-1.0.0.noarch.rpm
sudo yum -y install bzip2-devel \
                    curl-devel \
                    expat-devel \
                    freetype-devel \
                    gcc \
                    gcc-c++ \
                    gdbm-devel \
                    git \
                    libjpeg-turbo-devel \
                    libmemcached-devel \
                    libtiff-devel \
                    libxml2-devel \
                    libxslt-devel \
                    make \
                    openldap-devel \
                    openssl-devel \
                    poppler-devel \
                    readline-devel \
                    rpmdevtools \
                    sqlite-devel \
                    tk-devel \
                    unzip \
                    xerces-c-devel \
                    zlib-devel
