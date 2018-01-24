import sys
import easyrun


def main():
    easyrun.run('''ssh-keyscan -t rsa %s >> /root/.ssh/known_hosts; eval "$(ssh-agent)"; ssh-add awsczy.pem''' % sys.argv[1])
    

if __name__ == '__main__':
    main()
