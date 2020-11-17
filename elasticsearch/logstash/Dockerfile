ARG ELK_VERSION

# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash:${ELK_VERSION}

USER root
RUN yum remove -y java-11-openjdk-devel java-11-openjdk-headless-11.0.4.11-0.el7_6.x86_64 java-11-openjdk

RUN yum update -y

RUN yum install -y java-1.8.0-openjdk

COPY plugins/mysql-connector-java-5.1.49-bin.jar /usr/share/logstash/logstash-core/lib/jars

RUN ls -al /usr/share/logstash/logstash-core/lib/jars
RUN chown -R logstash:root /usr/share/logstash/logstash-core/lib/jars/mysql-connector-java-5.1.49-bin.jar 
RUN chmod -R 664 /usr/share/logstash/logstash-core/lib/jars/mysql-connector-java-5.1.49-bin.jar 

# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-input-jdbc
