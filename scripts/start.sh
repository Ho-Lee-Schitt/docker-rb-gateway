#!/bin/bash

if [ -z "$HTP_USER" ]
then
      echo "\$HTP_USER is empty. Failed to setup."
fi

if [ -z "$HTP_PSWD" ]
then
      echo "\$HTP_USER is empty. Failed to setup."
fi

htpasswd -b -c htpasswd $HTP_USER $HTP_PSWD

ssh-keygen -t rsa -N "" -b 4096 -f ~/.ssh/id_rsa -C "rb_gateway_docker@email.com" > /dev/null

echo ""
echo "Public Key generated:"
cat ~/.ssh/id_rsa.pub
echo ""

python3 ~/scripts/generate_config.py
if [ $? -ne 0 ]; then
	echo "Failed to setup"
	exit
fi

python3 ~/scripts/update_git_repos.py&

./rb-gateway
