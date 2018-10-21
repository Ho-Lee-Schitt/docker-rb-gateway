FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
    golang-go ssh git mercurial ca-certificates go-dep \
	apache2-utils python-pip && \
	pip install gitpython

RUN go get -d github.com/reviewboard/rb-gateway && \
    cd ~/go/src/github.com/reviewboard/rb-gateway && \
    mv sample_config.json config.json && dep ensure && \
    go build
	
EXPOSE 8888

COPY start.sh /start.sh
COPY generate_config.py /generate_config.py

RUN chmod +x /start.sh /generate_config.py

CMD /start.sh
