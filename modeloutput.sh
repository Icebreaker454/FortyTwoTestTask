#!/bin/sh

MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings

DATE=`date +%Y-%m-%d.%H.%M.%S`
FILE=$DATE.dat

PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$SETTINGS $MANAGE modeloutput 2>$FILE
