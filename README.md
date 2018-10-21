[![Build Status](https://travis-ci.com/Ho-Lee-Schitt/docker-rb-gateway.svg?token=vs3DEDeFykVr9Ydk7c1J&branch=master)](https://travis-ci.com/Ho-Lee-Schitt/docker-rb-gateway)

docker-rb-gateway
==================

Dockerised rb-gateway tool for Reviewboard.

    docker run --rm -d -p 8888:8888 -e HTP_USER=<htpasswd_username> -e HTP_PSWD=<htpasswd_password> -v <path_to_sources>:/git --name rb_gateway rb_gateway
