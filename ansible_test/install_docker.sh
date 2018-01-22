ansible dev --sudo -m shell -a 'wget -qO- https://get.docker.com/ | sh' -u ubuntu -i ./hosts
ansible dev --sudo -m shell -a 'docker pull alancao/node_server_image:1.0' -u ubuntu -i ./hosts
ansible dev --sudo -m shell -a 'mkdir /working' -u ubuntu -i ./hosts
ansible dev --sudo -m shell -a 'apt-get install python-pip -y' -u ubuntu -i ./hosts
ansible dev --sudo -m shell -a 'pip install docker-py' -u ubuntu -i ./hosts
