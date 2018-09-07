#!/usr/bin/env bash
###################
# Build CentOS 7
# docker run -v $PWD:/build -it centos:7.3.1611 /build/docker/build-vendor-libs.sh
# Build CentOS 6
# docker run -v $PWD:/build -it centos:6.7 /build/docker/build-vendor-libs.sh
###################

version="1.2.1"

# Important - "Do not adjust, versions are determined by whitelist"
lcms_ver="2.8"
gdal_ver="2.3.1"
geos_ver="3.6.0"
hdf5_ver="1.8.18"
libkml_ver="1.3.0"
netcdf_ver="4.4.1.1"
openjpeg_ver="2.1"
postgresql_ver="9.6.1"
proj_ver="4.9.3"
swig_ver="1.3.40"

HERE=$(dirname $(readlink -f $0))
source ${HERE}/utils.sh
set -eo pipefail

release=$(release)
cpu=$(cpu)
echo "-----------------"
echo "Release: $release"
echo "CPU: $cpu"
echo "-----------------"

yum -y install ant \
               autoconf \
               binutils \
               bison \
               bzip2 \
               bzip2-devel \
               centos-release-scl \
               chrpath \
               cmake \
               cppunit \
               curl-devel \
               db4-devel \
               expat-devel \
               flex \
               freetype-devel \
               gcc \
               gcc-c++ \
               gcc-gfortran \
               gdbm-devel \
               git \
               glibc-devel \
               krb5-devel \
               libcurl-devel \
               libgcj-devel \
               libjpeg-devel \
               libjpeg-turbo-devel \
               libpng-devel \
               libtiff-devel \
               libtool \
               libxml2-devel \
               libxslt-devel \
               make \
               ncurses-devel \
               openssl-devel \
               pam-devel \
               perl-devel \
               pkgconfig \
               poppler-devel \
               readline-devel \
               sqlite-devel \
               tar \
               tcl-devel \
               tk-devel \
               unzip \
               wget \
               xerces-c-devel

# Installing devtoolset-3-toolchain in order to stage GCC 4.9x which is required by GDAL 2.3.1
yum -y install wget && wget http://people.centos.org/tru/devtools-2/devtools-2.repo -O /etc/yum.repos.d/devtools-2.repo
yum -y install devtoolset-2-toolchain
. /opt/rh/devtoolset-2/enable
yum -y --enablerepo=centos-sclo-rh-testing install devtoolset-4-toolchain
. /opt/rh/devtoolset-4/enable

sandbox=/tmp/sandbox
vendor=/opt/boundless/vendor
mkdir -p $vendor/{bin,lib,include,share} $sandbox

if [[ $PATH != *$vendor* ]]; then
  export PATH=$PATH:$vendor/bin
fi

cd $sandbox

if [ ! -f hdf5-$hdf5_ver.tar.gz ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/hdf5-$hdf5_ver.tar.gz
fi
tar -xvf hdf5-$hdf5_ver.tar.gz
cd hdf5-$hdf5_ver
FC=/usr/bin/gfortran ./configure --disable-dependency-tracking \
            --enable-static=no \
            --enable-shared \
            --enable-cxx \
            --enable-fortran \
            --enable-f77 \
            --disable-f03 \
            --prefix=$vendor
make install
cd $sandbox

if [ ! -f netcdf-$netcdf_ver.tar.gz ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/netcdf-$netcdf_ver.tar.gz
fi
tar -xvf netcdf-$netcdf_ver.tar.gz
cd netcdf-$netcdf_ver
export CPATH=$vendor/include
export LIBRARY_PATH=$vendor/lib
export LD_LIBRARY_PATH=$vendor/lib
./configure --enable-shared \
            --enable-static=no \
            --prefix=$vendor
make install
cd $sandbox

if [ ! -f postgresql-$postgresql_ver.tar.gz ]; then
 wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/postgresql-$postgresql_ver.tar.gz
fi
tar -xvf postgresql-$postgresql_ver.tar.gz
cd postgresql-$postgresql_ver
sed --in-place '/fmgroids/d' src/include/Makefile
./configure --prefix=$vendor \
            --without-readline
make -C src/bin install
make -C src/include install
make -C src/interfaces install
cd $vendor/bin
rm -f clusterdb createdb createlang createuser dropdb droplang dropuser ecpg initdb \
      pg_archivecleanup pg_basebackup pg_controldata pg_ctl pg_dumpall pg_receivexlog \
      pg_recvlogical pg_resetxlog pg_rewind pg_test_fsync pg_test_timing pg_upgrade \
      pg_xlogdump pgbench reindexdb vacuumdb
cd $sandbox

if [ ! -f libkml-$libkml_ver.tar.gz ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/libkml-$libkml_ver.tar.gz
fi
tar -xvf libkml-$libkml_ver.tar.gz
cd libkml-$libkml_ver
if [ "$release" == "el6" ]; then
  sed -i "s|typedef voidpf|/**typedef voidpf|" src/kml/base/contrib/minizip/iomem_simple.h
  sed -i "/KMR/d" src/kml/base/contrib/minizip/iomem_simple.h
fi
sed -i "s|zlib.net|zlib.net/fossils|" cmake/External_zlib.cmake
cmake -DCMAKE_INSTALL_PREFIX:PATH=$vendor .
make install
cd $sandbox

if [ ! -f Little-CMS-lcms$lcms_ver.tar.gz ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/Little-CMS-lcms$lcms_ver.tar.gz
fi
tar -xvf Little-CMS-lcms$lcms_ver.tar.gz
cd Little-CMS-lcms$lcms_ver
./configure --enable-shared \
            --enable-static=no \
            --program-suffix=2 \
            --prefix=$vendor
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make install
cd $sandbox

if [ ! -f openjpeg-version.$openjpeg_ver.tar.gz ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/openjpeg-version.$openjpeg_ver.tar.gz
fi
tar -xvf openjpeg-version.$openjpeg_ver.tar.gz
cd openjpeg-version.$openjpeg_ver
cmake -DCMAKE_INSTALL_PREFIX:PATH=$vendor .
make install
cd $sandbox

if [ ! -f geos-$geos_ver.tar.bz2 ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/geos-$geos_ver.tar.bz2
fi
tar -xvf geos-$geos_ver.tar.bz2
cd geos-$geos_ver
./configure --prefix=$vendor \
            --enable-static=no \
            --enable-shared
make install
cd $sandbox

if [ ! -f proj-$proj_ver.tar.gz ]; then
  wget https://s3.amazonaws.com/boundless-packaging/whitelisted/src/proj-$proj_ver.tar.gz
fi
tar -xvf proj-$proj_ver.tar.gz
cd proj-$proj_ver/
./configure --prefix=$vendor \
            --enable-static=no \
            --enable-shared
make install
cd $sandbox

if [ ! -f gdal-$gdal_ver.tar.gz ]; then
  wget https://download.osgeo.org/gdal/2.3.1/gdal-$gdal_ver.tar.gz
fi
tar xf gdal-$gdal_ver.tar.gz
cd gdal-$gdal_ver/
./configure --prefix=$vendor \
    --with-jpeg \
    --with-png=internal \
    --with-geotiff=internal \
    --with-libtiff=internal \
    --with-libz=internal \
    --with-curl \
    --with-gif=internal \
    --with-geos=$vendor/bin/geos-config \
    --with-expat \
    --with-threads \
    --with-libkml=$vendor \
    --with-libkml-inc=$vendor/include/kml \
    --with-pg=$vendor/bin/pg_config \
    --with-openjpeg=$vendor \
    --with-netcdf=$vendor \
    --enable-static=no \
    --enable-shared
make
make install

rm -fr $vendor/include/boost
find $vendor/lib -type f -name '*.a' -exec rm -f {} +
find $vendor/lib -type f -name '*.la' -exec rm -f {} +

cd $vendor
tar -czf /build/vendor-$version-$release-$cpu.tar.gz *
