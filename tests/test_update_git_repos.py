import pytest
import os
import sys
from git import Repo
sys.path.insert(0, 'scripts')

from update_git_repos import sync_repo

CWD = os.getcwd()


def setup_function(module):
    test_folder = CWD + "/test_dir"
    os.mkdir(test_folder)


def teardown_function(module):
    test_folder = CWD + "/test_dir"
    os.system('rm -rf ' + test_folder)


def test_sync_updated_repo():
    test_folder = CWD + "/test_dir"
    git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython.git"), mirror=True)
    sync_repo(git_repo)


def test_stale_repo():
    test_folder = CWD + "/test_dir"
    git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython.git"), mirror=True)
    commit_shas = git_repo.git.log(format="format:%H", max_count=10)
    commit_sha_list = commit_shas.split('\n')
    git_repo.git.reset(commit_sha_list[int(len(commit_sha_list)/2)], soft=True)
    sync_repo(git_repo)
