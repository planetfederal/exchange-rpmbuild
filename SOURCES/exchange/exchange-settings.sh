#!/bin/bash

set -e

export PATH='/usr/pgsql-9.5/bin':$PATH
export SITE_URL='http://localhost/'
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
# export WGS84_MAP_CRS=True
# export AUTH_LDAP_SERVER_URI=
# export LDAP_SEARCH_DN=
# export AUTH_LDAP_USER=
# export AUTH_LDAP_BIND_DN=
# export AUTH_LDAP_BIND_PASSWORD=
# export REGISTRYURL=
