#!/bin/bash
NAME="basudebpur_agro_erp"                              #Name of the application (*)
DJANGODIR="`pwd`"                   # Django project directory (*)
SOCKFILE=`pipenv --venv`/bin/gunicorn.sock        # we will communicate using this unix socket (*)
USER="`whoami`"                                        # the user to run as (*)
#GROUP="webdata"                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=basudebpur_agro_erp.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=basudebpur_agro_erp.wsgi                     # WSGI module name (*)
echo "Starting $NAME as >>>> `whoami`"
# Activate the virtual environment
#cd $DJANGODIR
echo "inside project at path >>>> `pwd`"
source `pipenv --venv`/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
# Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec `pipenv --venv`/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
