#Builder
FROM golang:alpine AS builder
LABEL maintainer="nhughes030@gmail.com"

RUN apk update && \
    apk add --no-cache git mercurial dep

WORKDIR /go/src

RUN go get -d github.com/reviewboard/rb-gateway && \
    cd github.com/reviewboard/rb-gateway && \
    mv sample_config.json config.json && \
    dep ensure && \
    go build

# Worker
FROM alpine
LABEL maintainer="nhughes030@gmail.com"

RUN apk update && \
    apk add --no-cache   \
                    git \
                    apache2-utils \
                    bash \
                    openssh \
                    openssh-keygen \
                    python3-dev && \
    pip3 install gitpython

RUN addgroup -S rb_group && adduser -s /bin/bash -S rb_user -G rb_group
USER rb_user
WORKDIR /home/rb_user

COPY --from=builder /go/src/github.com/reviewboard/rb-gateway/rb-gateway rb-gateway

EXPOSE 8888

COPY --chown=rb_user:rb_group scripts scripts

RUN chmod +x scripts/start.sh scripts/generate_config.py scripts/update_git_repos.py

ENTRYPOINT [ "./scripts/start.sh" ]
