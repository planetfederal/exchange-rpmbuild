#!/bin/bash

set -e

if [[ $PATH != *"pgsql-9.6"* ]];then
  export PATH=$PATH:/usr/pgsql-9.6/bin
fi

export REGISTRY_DEBUG=${REGISTRY_DEBUG:-'True'}
export REGISTRY_SECRET_KEY=${REGISTRY_SECRET_KEY:-'Make sure you create a good secret key.'}
export REGISTRY_MAPPING_PRECISION=${REGISTRY_MAPPING_PRECISION:-'500m'}
export REGISTRY_SEARCH_URL=${REGISTRY_SEARCH_URL:-'http://127.0.0.1:9200'}
export REGISTRY_DATABASE_URL=${REGISTRY_DATABASE_URL:-'sqlite:////tmp/registry.db'}
export MAPPROXY_CACHE_DIR=${MAPPROXY_CACHE_DIR:-'/tmp'}
export REGISTRY_ALLOWED_IPS=${REGISTRY_ALLOWED_IPS:-'*'}

set +e
