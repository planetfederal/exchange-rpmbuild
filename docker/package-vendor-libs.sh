#!/usr/bin/env bash
###################
# Build CentOS 7
# docker run -v $PWD:/package -it centos:7.3.1611 /package/docker/package-vendor-libs.sh
# Build CentOS 6
# docker run -v $PWD:/package -it centos:6.7 /package/docker/package-vendor-libs.sh
###################

cd /package
rm -rf RPMS/* BUILD/* BUILDROOT/*

yum -y install bzip2 \
               rpmdevtools

QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define "_topdir /package" \
                                      --define "_sourcedir /package/SOURCES/vendor-libs" \
                                      -bb /package/SPECS/vendor-libs.spec
