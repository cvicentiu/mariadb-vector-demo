FROM debian:12
RUN echo 'deb-src http://deb.debian.org/debian bookworm main' > /etc/apt/sources.list
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install git --yes && apt-get build-dep mariadb-server --yes
RUN mkdir /mariadb/
WORKDIR /mariadb/
COPY ./clone_and_install.sh /mariadb/clone_and_install.sh
COPY ./create_demo_database.sql /mariadb/create_demo_database.sql
COPY ./prepare_data.sh /mariadb/prepare_data.sh
CMD bash

