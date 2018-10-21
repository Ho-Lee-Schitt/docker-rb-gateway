docker-rb-gateway
==================

Dockerised rb-gateway tool for Reviewboard.

    docker run --rm -d -p 8888:8888 -e HTP_USER=<htpasswd_username> -e HTP_PSWD=<htpasswd_password> -v <path_to_sources>:/git --name rb_gateway rb_gateway
