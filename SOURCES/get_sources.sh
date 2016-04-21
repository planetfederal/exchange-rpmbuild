#!/bin/bash

echo 'downloading sources'
echo '-------------------'

srcs=()
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geoserver/2.8/geoserver.war")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geoserver_data-geogig_od3.zip")

for src in "${srcs[@]}"
do
  filename=`echo $src | sed 's/.*\///'`
  if [[ ! -f $filename ]]
  then
    wget $src
  else
    echo $filename "already downloaded"
  fi
done

echo '-------------------'
echo 'finished get sources'
