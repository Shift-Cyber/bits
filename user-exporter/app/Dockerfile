FROM ubuntu:22.04

RUN [ "apt-get", "update"]
RUN [ "apt-get", "install", "python3", "sshpass", "python3-pip", "-y" ]

COPY * ./

RUN [ "pip3", "install", "-r", "requirements.txt" ]

CMD [ "bash", "run.sh" ] 