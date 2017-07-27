#!/bin/bash

set -e

<<<<<<< bc27c65f939ba7b1e18350aa41edc3bc2caa97f0
export SITEURL==${SITEURL:-'http://localhost/'}
export ES_URL=${ES_URL:-'http://localhost:9200/'}
export LOCKDOWN_GEONODE=${LOCKDOWN_GEONODE:-'True'}
export BROKER_URL=${BROKER_URL:-'amqp://guest:guest@localhost:5672/'}
export DATABASE_URL=${DATABASE_URL:-'postgres://exchange:boundless@localhost:5432/exchange'}
export POSTGIS_URL=${POSTGIS_URL:-'postgis://exchange:boundless@localhost:5432/exchange_data'}
export GEOSERVER_URL=${GEOSERVER_URL:-'http://localhost/geoserver/'}
export GEOSERVER_DATA_DIR=${GEOSERVER_DATA_DIR:-'/opt/geonode/geoserver_data'}
export GEOSERVER_LOG=${GEOSERVER_LOG:-'/opt/geonode/geoserver_data/logs/geoserver.log'}
export GEOGIG_DATASTORE_DIR=${GEOGIG_DATASTORE_DIR:-'/opt/geonode/geoserver_data/geogig'}
export DJANGO_LOG_LEVEL=${DJANGO_LOG_LEVEL:-'ERROR'}
export STATIC_ROOT=${STATIC_ROOT:-'/opt/boundless/exchange/.storage/static'}
export STATIC_URL=${STATIC_URL:-'/static/'}
export MEDIA_ROOT=${MEDIA_ROOT:-'/opt/boundless/exchange/.storage/media'}
export MEDIA_URL=${MEDIA_URL:-'/media/'}
export DEBUG_STATIC=${DEBUG_STATIC:-'False'}
export ALLOWED_HOSTS=${ALLOWED_HOSTS:-"['*']"}
export LANGUAGE_CODE=${LANGUAGE_CODE:-'en-us'}
export SOCIAL_BUTTONS=${SOCIAL_BUTTONS:-'False'}
export SECRET_KEY=${SECRET_KEY:-'exchange@q(6+mnr&=jb@z#)e_cix10b497vzaav61=de5@m3ewcj9%ctc'}
export DEFAULT_ANONYMOUS_VIEW_PERMISSION=${DEFAULT_ANONYMOUS_VIEW_PERMISSION:-'False'}
export DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION=${DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION:-'False'}
export WGS84_MAP_CRS=${WGS84_MAP_CRS:-'False'}

if [[ $PATH != *"pgsql-9.6"* ]];then
  export PATH=$PATH:/usr/pgsql-9.6/bin
fi

export SITEURL='http://localhost/'
export ES_URL='http://localhost:9200/'
export LOCKDOWN_GEONODE=True
export BROKER_URL='amqp://guest:guest@localhost:5672/'
export DATABASE_URL='postgres://exchange:boundless@localhost:5432/exchange'
export POSTGIS_URL='postgis://exchange:boundless@localhost:5432/exchange_data'
export GEOSERVER_URL='http://localhost/geoserver/'
export GEOSERVER_DATA_DIR='/opt/geonode/geoserver_data'
export GEOSERVER_LOG='/opt/geonode/geoserver_data/logs/geoserver.log'
export GEOGIG_DATASTORE_DIR='/opt/geonode/geoserver_data/geogig'
export DJANGO_LOG_LEVEL='ERROR'
export STATIC_ROOT='/opt/boundless/exchange/.storage/static_root'
export STATIC_URL='/static/'
export MEDIA_ROOT='/opt/boundless/exchange/.storage/media'
export MEDIA_URL='/media/'
export DEBUG_STATIC=False
export ALLOWED_HOSTS="['*']"
export LANGUAGE_CODE='en-us'
export SOCIAL_BUTTONS=False
export SECRET_KEY='exchange@q(6+mnr&=jb@z#)e_cix10b497vzaav61=de5@m3ewcj9%ctc'
export DEFAULT_ANONYMOUS_VIEW_PERMISSION=False
export DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION=False
export ON_AIRGAPPED_NETWORK=False
# export WGS84_MAP_CRS=True
# export AUTH_LDAP_SERVER_URI=
# export AUTH_LDAP_BIND_PASSWORD=
# export AUTH_LDAP_BIND_DN=
# export LDAP_SEARCH_DN=
# export REGISTRYURL=

set +e
