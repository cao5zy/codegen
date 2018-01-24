import boto3
import sys

def main():
    print((lambda instances:list(map(lambda instance:{"id":instance.id, "ip":instance.public_ip_address},instances)))  \
        (boto3.resource('ec2').instances.filter(Filters=[{'Name':'instance-state-name', 'Values':['running']}])))


if __name__ == '__main__':
    main()
