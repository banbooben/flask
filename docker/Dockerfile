FROM lnpy3:latest

ENV PROJECT_NAME "flaskr"

RUN mkdir /${PROJECT_NAME}
WORKDIR /${PROJECT_NAME}
COPY ./${PROJECT_NAME}/ /${PROJECT_NAME}/


# 安装supervisor
RUN apt-get install -y supervisor openssh-server  \
    && mkdir -p /var/log/supervisor \
    && mkdir -p /run/sshd \
    && cp /${PROJECT_NAME}/deploy/flask_supervisor_config.conf /etc/supervisor/conf.d/flask_supervisor_config.conf


RUN chmod -R 777 /${PROJECT_NAME}/ \
    && pip3 install --no-cache-dir -r /${PROJECT_NAME}/deploy/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mv /${PROJECT_NAME}/deploy/default /etc/nginx/sites-available/default
#    && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default \
#    && /usr/sbin/nginx -s reload

#CMD python3 /${PROJECT_NAME}/manage.py runserver -h 0.0.0.0 -p 5000 --threaded
#CMD sh /${PROJECT_NAME}/init_database.sh && uwsgi  --ini /${PROJECT_NAME}/uwsgi.ini && nginx -g "daemon off;"
CMD /usr/bin/supervisord