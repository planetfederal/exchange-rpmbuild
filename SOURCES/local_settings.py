# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from exchange.settings import *

SITENAME = 'Exchange'
SITEURL = 'http://localhost/'
DEBUG = False

ALLOWED_HOSTS = ['localhost']

PROXY_ALLOWED_HOSTS = (
'*',
)

CLASSIFICATION_BANNER_ENABLED = False
CLASSIFICATION_TEXT = ''
CLASSIFICATION_TEXT_COLOR = ''
CLASSIFICATION_BACKGROUND_COLOR = ''
CLASSIFICATION_LINK = ''
DEFAULT_MAP_CRS = "EPSG:900913"
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
REGISTRATION_OPEN = False


DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'exchange'
DATABASE_USER = 'exchange'
DATABASE_PASSWORD = 'THE_DATABASE_PASSWORD'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    },
    'exchange_imports': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'exchange_data',
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}

GEOSERVER_URL = SITEURL + 'geoserver/'

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : GEOSERVER_URL,
        'PUBLIC_LOCATION' : GEOSERVER_URL,
        'USER' : 'admin',
        'PASSWORD' : 'geoserver',
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINT_NG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIG_ENABLED' : True,
        'WMST_ENABLED' : False,
        'DATASTORE': 'exchange_imports',
        'GEOGIG_DATASTORE_DIR':'/var/lib/geoserver_data/geogig',
    }
}

#  Database datastore connection settings
GEOGIG_DATASTORE_NAME = 'geogig-repo'

GEOSERVER_BASE_URL = OGC_SERVER['default']['LOCATION'] + "wms"

MAP_BASELAYERS = [
    {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": GEOSERVER_BASE_URL,
            "restUrl": "/gs/rest",
            "name": "local geoserver"
        }
    },
    {
        "source": {"ptype": "gxp_osmsource", "name": "OpenStreetMap"},
        "type": "OpenLayers.Layer.OSM",
        "name": "mapnik",
        "title": "OpenStreetMap",
        "args": ["OpenStreetMap"],
        "visibility": True,
        "fixed": True,
        "group":"background"
    }
]

UPLOADER = {
    'BACKEND' : 'geonode.importer',
    'OPTIONS' : {
        'TIME_ENABLED' : True,
        'GEOGIG_ENABLED' : True,
    }
}

MEDIA_ROOT = '/var/lib/geonode/django/media'
STATIC_ROOT = '/var/lib/geonode/django/static'

# CSW settings
CATALOGUE = {
    'default': {
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        'URL': '%scatalogue/csw' % SITEURL,
    }
}

BROKER_URL = 'amqp://guest@127.0.0.1:5672'
CELERY_ALWAYS_EAGER = False
NOTIFICATION_QUEUE_ALL = not CELERY_ALWAYS_EAGER
NOTIFICATION_LOCK_LOCATION = '/var/lib/geonode/gunicorn'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'geonode',
        },
}

INSTALLED_APPS += (
    'haystack',
)

SLACK_ENABLED = False
SLACK_WEBHOOK_URLS = ['']
