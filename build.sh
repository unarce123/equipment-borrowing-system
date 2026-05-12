#!/usr/bin/env bash

py -m pip install -r requirements.txt

py manage.py collectstatic --noinput

py manage.py migrate