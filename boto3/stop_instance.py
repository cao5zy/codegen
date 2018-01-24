import boto3
import sys

def main():
    
    (lambda instances:list(map(lambda instance:(lambda x, y:x)(instance.stop(), instance.terminate()), instances))) \
        (boto3.resource('ec2').instances.filter(InstanceIds=[sys.argv[1]]))


if __name__ == '__main__':
    main()
