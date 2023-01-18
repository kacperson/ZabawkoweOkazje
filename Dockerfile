FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install python3-pip -y
RUN apt-get install -y tzdata
RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod 7777 /code/stronka/ceneo/chromedriver
RUN cp -r /code/stronka /usr/local/lib/python3.8/dist-packages

CMD [ "python3", "app.py" ]
