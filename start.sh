#!bin/bash

htpasswd -b -c ~/go/src/github.com/reviewboard/rb-gateway/htpasswd $HTP_USER $HTP_PSWD

ssh-keygen -t rsa -N "" -b 4096 -f /root/.ssh/id_rsa -C "rb_gateway_docker@email.com" > /dev/null

echo ""
echo "Public Key generated:"
cat ~/.ssh/id_rsa.pub
echo ""

python generate_config.py
if [ $? -ne 0 ]; then
	echo "Failed to setup"
	return 1
fi

cd /root/go/src/github.com/reviewboard/rb-gateway;
./rb-gateway
