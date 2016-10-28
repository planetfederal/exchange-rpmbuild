# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
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

import os
from exchange.settings import *  # noqa


ALLOWED_HOSTS = ['*']
DEBUG = False
SECRET_KEY = 'exchange@q(6+mnr&=jb@z#)e_cix10b497vzaav61=de5@m3ewcj9%ctc'

WSGI_APPLICATION = "exchange.wsgi.application"
ROOT_URLCONF = 'exchange.urls'

LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(LOCAL_ROOT, os.pardir)

# static files storage
STATICFILES_DIRS.append(os.path.join(LOCAL_ROOT, "static"),)  # noqa
STATIC_ROOT = os.path.join(PROJECT_ROOT, '.storage/static')
STATIC_URL = '/static/'

# media file storage
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '.storage/media')
MEDIA_URL = '/uploaded/'

# installed applications
INSTALLED_APPS = (
    'exchange',
) + INSTALLED_APPS  # noqa

# update local template dir for overides
TEMPLATES[0]['DIRS'] = [os.path.join(LOCAL_ROOT, 'templates')]  # noqa
