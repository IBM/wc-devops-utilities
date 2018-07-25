FROM docker:dind

RUN apk --no-cache add make && apk --no-cache add sed && apk --no-cache add bash&& apk --no-cache add python3 && pip3 install jinja2  argparse requests docker datetime hvac kubernetes pyyaml && mkdir /root/.helm

COPY ./commerce-devops-utilities /commerce-devops-utilities

COPY ./entrypoint.sh /

#COPY ./.helm /root/.helm

COPY ./helm /usr/bin

RUN  chmod 777 /entrypoint.sh /usr/bin/helm /commerce-devops-utilities && \
     ln -s /usr/bin/python3.6 /usr/bin/python

#CMD /entrypoint.sh
