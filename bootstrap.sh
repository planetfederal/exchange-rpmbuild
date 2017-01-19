#!/usr/bin/env bash

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
                    bzip2-devel \
                    curl-devel \
                    expat-devel \
                    freetype-devel \
                    libjpeg-turbo-devel \
                    libtiff-devel \
                    libxml2-devel \
                    libxslt-devel \
                    openldap-devel \
                    poppler-devel \
                    python-devel \
                    python-virtualenv \
                    python27-devel \
                    python27-virtualenv \
                    qlite-devel \
                    xerces-c-devel \
                    zlib-devel \
                    unzip \
                    git \
                    rpmdevtools
