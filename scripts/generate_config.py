import os
import json
import re
import sys
from git import Repo
from subprocess import check_output

cwd = os.getcwd()
git_dir = "/git/"
git_repos = os.listdir(git_dir)

known_hosts = []

config_file = { "htpasswdPath": "htpasswd",
                "port": 8888,
                "tokenStorePath": "tokens.dat",
                "webhookStorePath": "webhooks.json",
                "repositories" : []
}

regexer = re.compile('.*@(.*):.*')

for folder in git_repos:
    bare_repo = Repo(os.path.join(git_dir, folder))
    if bare_repo.bare:
        m = regexer.match(bare_repo.remotes.origin.url)
        new_host = str(m.group(1))
        if new_host not in known_hosts:
            known_hosts.append(new_host)
            host_data = check_output(["ssh-keyscan", new_host])
            kh = open(cwd + "/.ssh/known_hosts", "a")
            kh.write(host_data)
            kh.close()
        config_file["repositories"].append({"name": folder, "path": git_dir+folder, "scm": "git"})

if not config_file["repositories"]:
    sys.exit(1)
    
with open(cwd +  "/go/src/github.com/reviewboard/rb-gateway/config.json", "w") as fp:
    json.dump(config_file, fp)
