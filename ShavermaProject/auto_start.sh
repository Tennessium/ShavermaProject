#!/bin/bash
source /root/django_venv/bin/activate
while :
do
	python manage.py runserver 127.0.0.1:8000
done
