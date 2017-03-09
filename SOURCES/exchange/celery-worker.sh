#!/bin/bash

source /etc/profile.d/exchange-settings.sh
source /etc/profile.d/vendor-libs.sh
cd /opt/boundless/exchange
source .venv/bin/activate
celery worker --app=exchange.celery_app --uid=exchange --loglevel=info
