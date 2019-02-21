import pytest
import os
import sys
from git import Repo
sys.path.insert(0, 'scripts')

from generate_config import generate_config

CWD = os.getcwd()

def setup_function(module):
    test_folder = CWD + "/test_dir"
    os.mkdir(test_folder)


def teardown_function(module):
    test_folder = CWD + "/test_dir"
    os.system('rm -rf ' + test_folder)


def test_empty_config():
    test_folder = CWD + "/test_dir"
    test_config = generate_config(test_folder, False)
    assert test_config == None


def test_config_with_one_entry():
    test_folder = CWD + "/test_dir"
    git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython.git"), mirror=True)
    git_repo.remotes.origin.add_url("git@github.com:gitpython-developers/GitPython.git")
    git_repo.remotes.origin.delete_url("https://github.com/gitpython-developers/GitPython.git")
    
    test_config = generate_config(test_folder, False)
    assert test_config != None


def test_config_with_http_entry():
    test_folder = CWD + "/test_dir"
    git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython.git"), mirror=True)
    
    test_config = generate_config(test_folder, False)
    assert test_config == None


def test_config_with_multiple_ssh_entries():
    test_folder = CWD + "/test_dir"
    for i in range(3):
        git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython" + str(i) + ".git"), mirror=True)
        git_repo.remotes.origin.add_url("git@github.com:gitpython-developers/GitPython.git")
        git_repo.remotes.origin.delete_url("https://github.com/gitpython-developers/GitPython.git")
    
    test_config = generate_config(test_folder, False)
    assert test_config != None


def test_config_with_multiple_http_entries():
    test_folder = CWD + "/test_dir"
    for i in range(3):
        git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython" + str(i) + ".git"), mirror=True)
    
    test_config = generate_config(test_folder, False)
    assert test_config == None


def test_config_with_mixture_of_entries():
    test_folder = CWD + "/test_dir"
    for i in range(4):
        git_repo = Repo.clone_from("https://github.com/gitpython-developers/GitPython.git", str(test_folder + "/GitPython" + str(i) + ".git"), mirror=True)
        if (i % 2) == 0:
            git_repo.remotes.origin.add_url("git@github.com:gitpython-developers/GitPython.git")
            git_repo.remotes.origin.delete_url("https://github.com/gitpython-developers/GitPython.git")
    
    test_config = generate_config(test_folder, False)
    assert test_config != None
