import boto3

def main():
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(ImageId="ami-d7df06b9", MinCount=1, MaxCount=1, KeyName="aws.czy")[0]
    print({'id':instance.id, 'ip':instance.public_ip_address})
    


if __name__ == '__main__':
    main()
