FROM python:3.10-bullseye

RUN [ "mkdir","-p","/app" ]

COPY app/ .

RUN pip3 install -r requirements.txt

CMD [ "python3", "bot.py"]