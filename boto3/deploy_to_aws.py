import boto3
import easyrun
import sys
import getopt
import time

def getParam(paramName):
    def getKeyVal(options):
        return [(key, val) for (key, val) in options if key == "--" + paramName]

    return (lambda options:options[0][1] if len(options) > 0 else None)\
        (getKeyVal(getopt.getopt(sys.argv[1:], "i:k:m:", ["imageid=", "keypairename=", "meta_addr="])[0]))

def getInstance(ec2, instanceId):
    return (lambda instances:instances[0] if len(instances) > 0 else None)\
        (list(filter(lambda instance:instance.id == instanceId, ec2.instances.filter(Filters=[{'Name':'instance-state-name', 'Values':['running']}]))))

def createAWSInstance(ec2):
    def create(instance, count):
       latestInstance = lambda:getInstance(ec2, instance.id)

       while count < 300:
           count += 1
           if latestInstance() and latestInstance().public_ip_address and latestInstance().state['Code'] == 16:
               print('pause a bit')
               time.sleep(10)
               print('continue')
               return latestInstance().public_ip_address
           print('waiting')
           time.sleep(3)

       return None
    return create(ec2.create_instances(ImageId=getParam("imageid"), MinCount=1, MaxCount=1, KeyName=getParam("keypairename"))[0], 0)


def writeIp(ip_addr):
    with open("./hosts", 'w') as file:
        file.write("[dev]\n")
        file.write(ip_addr)
        
    return ip_addr

def deployToAws(ip_addr):
    easyrun.run('''ssh-keyscan -t rsa %s >> /root/.ssh/known_hosts;sleep 1s; eval "$(ssh-agent)";sleep 1s; ssh-add awsczy.pem;sleep 1s;ansible-playbook -i ./hosts -u ubuntu prepareEnv.yml;sleep 1s;ansible-playbook -i ./hosts -u ubuntu root.yml''' % ip_addr)
    return ip_addr

def generateCode(ip_addr):
    def downloadMeta():
        easyrun.run('curl %s -o md.config' % getParam("meta_addr"))

    def generateCode():
        easyrun.run('''initservice.sh''')

    return (lambda x,y:ip_addr)\
        (downloadMeta(),generateCode())
    

    


def main():
    print('deploy completed at %s' % (lambda ec2:deployToAws(generateCode(writeIp((createAWSInstance(ec2))))))\
        (boto3.resource('ec2')))


if __name__ == '__main__':
    main()
