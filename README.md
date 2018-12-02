[![Build Status](https://travis-ci.com/Ho-Lee-Schitt/docker-rb-gateway.svg?token=vs3DEDeFykVr9Ydk7c1J&branch=master)](https://travis-ci.com/Ho-Lee-Schitt/docker-rb-gateway)

docker-rb-gateway
==================

Dockerised rb-gateway tool for Reviewboard.

    docker run  --rm -d \
                -p 8888:8888 \
                -e HTP_USER=<htpasswd_username> \
                -e HTP_PSWD=<htpasswd_password> \
                -v <path_to_sources>:/git \
                --name rb_gateway \
                rb_gateway

## Environment Variables

The container accepts the following environment variables:

- ```HTP_USER``` - the username that will be used to create the htpasswd file.
- ```HTP_PSWD``` - the password that will be used to create the htpasswd file.

This container has one volume mount-point:

- `/git` - The path where the the git repos are stored in the container.

## TODO
- Add support for Mercurial Repos.
