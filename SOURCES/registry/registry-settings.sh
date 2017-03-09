#!/bin/bash

set -e

source /etc/profile.d/vendor-libs.sh

export REGISTRY_DEBUG=${REGISTRY_DEBUG:-'False'}
export REGISTRY_SECRET_KEY=${REGISTRY_SECRET_KEY:-'Make sure you create a good secret key.'}
export REGISTRY_MAPPING_PRECISION=${REGISTRY_MAPPING_PRECISION:-'500m'}
export REGISTRY_SEARCH_URL=${REGISTRY_SEARCH_URL:-'http://127.0.0.1:9200'}
export REGISTRY_DATABASE_URL=${REGISTRY_DATABASE_URL:-'postgres://registry:boundless@localhost:5432/registry'}
export MAPPROXY_CACHE_DIR=${MAPPROXY_CACHE_DIR:-'/tmp'}
export REGISTRY_ALLOWED_IPS=${REGISTRY_ALLOWED_IPS:-'*'}

set +e
