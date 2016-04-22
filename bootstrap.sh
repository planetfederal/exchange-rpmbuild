#!/usr/bin/env bash

# Need to change to a new exchange repo
curl -o /etc/yum.repos.d/exchange.repo https://yum.boundlessps.com/geoshape.repo
sudo yum -y update
sudo yum -y install python27-devel \
                    python27-virtualenv \
                    gcc \
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
                    createrepo

pushd /vagrant/SOURCES
./get_sources.sh
popd
