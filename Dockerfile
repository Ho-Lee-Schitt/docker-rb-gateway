FROM ubuntu:18.04
MAINTAINER nhughes030@gmail.com

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
                    apache2-utils \
                    bash \
                    ca-certificates \
                    git \
                    go-dep \
                    golang-go \
                    mercurial \
                    python3 \
                    python3-pip \
                    ssh && \
    pip3 install gitpython

RUN useradd -ms /bin/bash rb_user
USER rb_user
WORKDIR /home/rb_user
    
RUN go get -d github.com/reviewboard/rb-gateway && \
    cd ~/go/src/github.com/reviewboard/rb-gateway && \
    mv sample_config.json config.json && \
    dep ensure && \
    go build
    
EXPOSE 8888

COPY --chown=rb_user scripts scripts

RUN chmod +x scripts/start.sh scripts/generate_config.py scripts/update_git_repos.py

CMD bash /home/rb_user/scripts/start.sh
