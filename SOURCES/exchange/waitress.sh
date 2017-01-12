#!/bin/bash

source /etc/profile.d/exchange-settings.sh
cd /opt/boundless/exchange
source .venv/bin/activate
/opt/boundless/exchange/.venv/bin/waitress-serve --port=8000 bex.wsgi:application
