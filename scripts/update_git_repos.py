import os
from queue import Queue
from threading import Thread
from git import Repo, exc
from time import sleep


def sync_repo(git_repo):
    try:
        git_repo.remote("origin").fetch("-p")
    except exc.GitCommandError:
        print("Auth Error. Please add generated Public Key to Remote Service")


def worker():
    while True:
        item = q.get()
        sync_repo(item)
        print("Repo Synced")
        q.task_done()


num_worker_threads = 10
cwd = os.getcwd()
git_dir = "/git/"
git_repos = os.listdir(git_dir)
repo_list = []

for folder in git_repos:
    bare_repo = Repo(os.path.join(git_dir, folder))
    if bare_repo.bare:
        repo_list.append(bare_repo)

if num_worker_threads > len(repo_list):
    actual_worker_count = len(repo_list)
else:
    actual_worker_count = num_worker_threads

q = Queue()
for i in range(actual_worker_count):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

while True:
    for repo in repo_list:
        q.put(repo)

    q.join() 
    sleep(300)
