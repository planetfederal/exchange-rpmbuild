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

WSGI_APPLICATION = "exchange.wsgi.application"
ROOT_URLCONF = 'exchange.urls'

LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

# installed applications
INSTALLED_APPS = (
    'exchange',
) + INSTALLED_APPS  # noqa

# update local template dir for overides
TEMPLATES[0]['DIRS'] = [os.path.join(LOCAL_ROOT, 'templates')]  # noqa
