#!/usr/bin/env bash

set -eo pipefail

version="1.2.0"
sandbox=/tmp/sandbox
vendor=/opt/boundless/vendor
mkdir -p $vendor/{bin,lib,include,share} $sandbox

# build and install hdf5-devel (version 1.8.18)
wget http://hdf4.org/ftp/HDF5/current18/src/hdf5-1.8.18.tar.gz
tar -xvf hdf5-1.8.18.tar.gz
cd hdf5-1.8.18
FC=/usr/bin/gfortran ./configure --disable-dependency-tracking \
            --enable-static=no \
            --enable-shared \
            --enable-cxx \
            --enable-fortran \
            --prefix=$vendor
make install
cd $sandbox

# build and install netcdf-devel (version 4.4.1.1)
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.4.1.1.tar.gz
tar -xvf netcdf-4.4.1.1.tar.gz
cd netcdf-4.4.1.1
export CPPFLAGS='-I/opt/boundless/vendor/include'
export LDFLAGS='-L/opt/boundless/vendor/lib'
./configure --enable-shared \
            --enable-static=no \
            --prefix=$vendor
make install
cd $sandbox

# build and install postgresql-devel (version 9.6.1)
wget https://ftp.postgresql.org/pub/source/v9.6.1/postgresql-9.6.1.tar.gz
tar -xvf postgresql-9.6.1.tar.gz
cd postgresql-9.6.1
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

# build and install libkml-devel (version 1.3.0)
wget https://github.com/libkml/libkml/archive/1.3.0.tar.gz
tar -xvf 1.3.0.tar.gz
cd libkml-1.3.0
sed -i "s|zlib.net|zlib.net/fossils|" cmake/External_zlib.cmake
cmake -DCMAKE_INSTALL_PREFIX:PATH=$vendor .
make install
cd $sandbox

# build and install lcms2-devel (version 2.8)
wget https://github.com/mm2/Little-CMS/archive/lcms2.8.tar.gz
tar -xvf lcms2.8.tar.gz
cd Little-CMS-lcms2.8
./configure --enable-shared \
            --enable-static=no \
            --program-suffix=2 \
            --prefix=$vendor
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make install
cd $sandbox

# build and install openjpeg2-devel (version 2.1)
wget https://github.com/uclouvain/openjpeg/archive/version.2.1.tar.gz
tar -xvf version.2.1.tar.gz
cd openjpeg-version.2.1
cmake -DCMAKE_INSTALL_PREFIX:PATH=$vendor .
make install
cd $sandbox

# build and install geos-devel (version 3.6.0)
wget http://download.osgeo.org/geos/geos-3.6.0.tar.bz2
tar -xvf geos-3.6.0.tar.bz2
cd geos-3.6.0
./configure --prefix=$vendor \
            --enable-static=no \
            --enable-shared
make install
cd $sandbox

# build and install proj-devel (version 4.9.3)
wget http://download.osgeo.org/proj/proj-4.9.3.tar.gz
tar -xvf proj-4.9.3.tar.gz
cd proj-4.9.3/
./configure --prefix=$vendor \
            --enable-static=no \
            --enable-shared
make install
cd $sandbox

# build and install swig (version 1.3.40)
wget https://sourceforge.net/projects/swig/files/swig/swig-1.3.40/swig-1.3.40.tar.gz
tar -xvf swig-1.3.40.tar.gz
cd swig-1.3.40
./configure --prefix=$vendor
make
make install
cd $sandbox

# build and install gdal (version 2.1.2)
wget http://download.osgeo.org/gdal/2.1.2/gdal-2.1.2.tar.gz
tar xf gdal-2.1.2.tar.gz
cd gdal-2.1.2/
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
cd swig/java
sed -i 's|SWIG = swig|SWIG = /opt/boundless/vendor/bin/swig|' ../SWIGmake.base
sed -i '1iJAVA_HOME=/usr/lib/jvm/java-openjdk' java.opt
make
make install
cd $sandbox

# cleanup non essential boost headers
rm -fr $vendor/include/boost

# remove static libraries
find $vendor/lib -type f -name '*.a' -exec rm -f {} +
find $vendor/lib -type f -name '*.la' -exec rm -f {} +

# tar up directory
cd /opt/boundless/vendor
tar -czf /app/vendor-${version}-el7.tar.gz *
