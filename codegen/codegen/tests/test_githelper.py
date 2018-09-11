from nose import with_setup
from assertpy import assert_that
from codegenhelper import put_folder, remove_test_folder, init_test_folder, test_root
from ..githelper import has_uncommit, cmd
import subprocess
import os

def cmd(command, cwd):
    return subprocess.call(command, shell=True, cwd=cwd)

project_name = "test1"
def setup_folder_with_uncommit():
    init_test_folder()

    cmd("git init %s" % project_name, test_root())
    cmd('echo hello >> test.txt', os.path.join(test_root(), project_name))
    cmd('git add .', os.path.join(test_root(), project_name))
    cmd('git commit . -m "commit"', os.path.join(test_root(), project_name))
    cmd('echo hello11 >> test.txt', os.path.join(test_root(), project_name))

def setup_folder_with_committed():
    init_test_folder()
    cmd("git init %s" % project_name, test_root())
    cmd('echo hello >> test.txt', os.path.join(test_root(), project_name))
    cmd('git add .', os.path.join(test_root(), project_name))
    cmd('git commit . -m "commit"', os.path.join(test_root(), project_name))

def setup_folder_with_no_git():
    init_test_folder()
    cmd('mkdir %s' % project_name, test_root())
    
@with_setup(setup_folder_with_uncommit, remove_test_folder)
def test_has_uncommit_true():
    assert_that(has_uncommit(os.path.join(test_root(), project_name))).is_true()

@with_setup(setup_folder_with_committed, remove_test_folder)
def test_has_uncommit_false():
    assert_that(has_uncommit(os.path.join(test_root(), project_name))).is_false()

@with_setup(setup_folder_with_no_git, remove_test_folder)
def test_has_repo_false():
    assert_that(has_uncommit(os.path.join(test_root(), project_name))).is_true()
