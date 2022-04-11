#!/bin/bash

# uwsgi --ini /flaskr/deploy/uwsgi.ini  && service nginx start && celery -A celery_task.celery_process.celery_app worker -l info -f /flaskr/app/logs/celery.log

#service nginx start && uwsgi --ini /flaskr/deploy/uwsgi.ini && celery -A celery_task.celery_process.celery_app worker -l info
#
#echo "start nginx server"
#$(service nginx start)
#echo "start web_api by uwsgi"
#$(uwsgi --ini /flaskr/deploy/uwsgi.ini)
#
echo "start celery"
$(celery -A application.extensions.celery_task.celery_process.celery_app worker -l info)


#echo "start web_api by uwsgi"
#$(uwsgi --ini /flaskr/deploy/uwsgi.ini)
#
#echo "start nginx server"
#$(nginx -g "daemon off;")



#echo "start nginx server"
#service nginx start
#echo "start web_api by uwsgi"
#uwsgi --ini /flaskr/deploy/uwsgi.ini