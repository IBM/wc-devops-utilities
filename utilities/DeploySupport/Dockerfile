#Need a base python docker
#Install kubernetes python client
#Install the python scripts develped for ( check dependence / create and check secure / create and check PVC )
FROM python:3.6-alpine3.6

COPY ./kube-python /kube-python
RUN  apk add --update openssl && \
     pip install kubernetes argparse requests pyyaml && \
     chmod -R 755 /kube-python && \
     rm -rf /var/cache/apk/*

ENTRYPOINT ["python", "/kube-python/kubcli.py"]
