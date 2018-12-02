import os
from queue import Queue
from threading import Thread
from git import Repo
from time import sleep


def sync_repo(git_repo):
    git_repo.remote().fetch()


def worker():
    while True:
        item = q.get()
        sync_repo(item)
        q.task_done()


num_worker_threads = 10
cwd = os.getcwd()
git_dir = "/git/"
git_repos = os.listdir(git_dir)
repo_list = []

while True:
    for folder in git_repos:
        bare_repo = Repo(os.path.join(git_dir, folder))
        if bare_repo.bare:
            repo_list.append(bare_repo)

    q = Queue()
    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    for repo in repo_list:
        q.put(repo)

    q.join() 
    sleep(600)
