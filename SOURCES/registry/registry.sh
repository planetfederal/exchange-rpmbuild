#!/bin/bash

source /etc/profile.d/registry-settings.sh
/opt/registry/.venv/bin/python /opt/registry/registry.py runserver 0.0.0.0:8001
