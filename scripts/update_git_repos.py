import os
import sys
from queue import Queue
from threading import Thread
from git import Repo, exc
from time import sleep


def sync_repo(git_repo):
    try:
        git_repo.remote("origin").update()
    except exc.GitCommandError:
        print("Auth Error. Please add generated Public Key to Remote Service")


def worker():
    while True:
        item = q.get()
        sync_repo(item)
        q.task_done()


if __name__ == '__main__':
    num_worker_threads = int(os.getenv('THREAD_LIMIT', 10))
    cwd = os.getcwd()
    git_dir = "/git/"
    git_repos = os.listdir(git_dir)
    repo_list = []

    if num_worker_threads == 0:
        sys.exit(0)

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
