#!/bin/bash
FROM python_base:v1
MAINTAINER courstick@gmail.com
ARG project_name=xx_official_website

ADD . /srv/project
WORKDIR /srv/project/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD dockerfiles/supervisor.conf /etc/supervisor/conf.d/${project_name}.conf

RUN /usr/bin/supervisord -c /etc/supervisor/supervisord.conf

CMD ["bash"]
