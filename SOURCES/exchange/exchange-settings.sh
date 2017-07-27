#!/bin/bash

set -e

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
# export LDAP_SEARCH_DN=
# export AUTH_LDAP_USER=
# export AUTH_LDAP_BIND_DN=
# export AUTH_LDAP_BIND_PASSWORD=
# export REGISTRYURL=

set +e
