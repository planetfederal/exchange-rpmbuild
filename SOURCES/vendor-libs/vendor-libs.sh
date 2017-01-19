#!/bin/bash

set +e

export LIBKML_LIBS="${LIBRARY_PATH}"
export GDAL_DATA="/opt/boundless/vendor/share/gdal"
export PROJ_LIB="/opt/boundless/vendor/share/proj"
export GEOS_LIBRARY_PATH="/opt/boundless/vendor/lib"
export PATH="/opt/boundless/vendor/bin":"${PATH}"
export LD_LIBRARY_PATH="/opt/boundless/vendor/lib":"${LD_LIBRARY_PATH}"
