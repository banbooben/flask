#!/bin/bash

echo "SERVICE RUN STATUS: ONLINE !!!"
cd $(dirname $0)/../application
gunicorn manage:app -c config/gunicorn_conf.py




