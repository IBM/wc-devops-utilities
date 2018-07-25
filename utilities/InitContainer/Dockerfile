FROM  centos:latest
RUN yum update -y && yum install -y bc && yum clean all
ADD ./entrypoint.sh /
CMD /entrypoint.sh
