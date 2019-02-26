import os
import json
import re
import sys
from git import Repo
from subprocess import check_output

GIT_BASE_DIR = '/git/'
CWD = os.getcwd()
UPDATE_HOSTFILE = True

def generate_config(git_dir, update_hosts):
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
            if not m:
                continue
            if update_hosts:
                new_host = str(m.group(1))
                add_host_to_hostfile(new_host, known_hosts)

            config_file["repositories"].append({"name": folder, "path": git_dir+folder, "scm": "git"})

    if not config_file["repositories"]:
        print("No repositories found")
        return None
    else:
        return config_file


def add_host_to_hostfile(new_host, known_hosts):
    if new_host not in known_hosts:
                known_hosts.append(new_host)
                host_data = check_output(["ssh-keyscan", new_host])
                kh = open(CWD + "/.ssh/known_hosts", "a")
                kh.write(host_data.decode("utf-8"))
                kh.close()


if __name__ == '__main__':
    config_json = generate_config(GIT_BASE_DIR, UPDATE_HOSTFILE)
    if config_json:
        with open(CWD +  "/config.json", "w") as fp:
            json.dump(config_json, fp)
