#!/bin/bash

set -e

export REGISTRY_DEBUG=True
export REGISTRY_SECRET_KEY='Make sure you create a good secret key.'
export REGISTRY_MAPPING_PRECISION='500m'
export REGISTRY_SEARCH_URL='http://127.0.0.1:9200'
export REGISTRY_DATABASE_URL='sqlite:////tmp/registry.db'
export MAPPROXY_CACHE_DIR='/tmp'
export REGISTRY_ALLOWED_IPS='*'

set +e
