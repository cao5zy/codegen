#! /bin/python
import util
from jinja2 import Template
import flattener

def addBase(filePath):
    template = '''---

- name: init test environment
  hosts: localhost
  become: true
  become_method: sudo

  tasks:
 '''

    with open(filePath, 'a') as file:
        file.write(template)

def addUnitTests(filePath):
    with open(filePath, 'a') as file:
        file.write('''    - name: spec tests
      shell: source /home/caozy/.nvm/nvm.sh && nvm use v6.10.3 && 
      args:
        executable: /bin/bash''')

