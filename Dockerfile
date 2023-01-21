FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install python3-pip -y
RUN apt-get install -y tzdata unzip
RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
COPY . /code/
WORKDIR /code/stronka/ceneo
RUN wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip
RUN unzip -o chromedriver_linux64.zip
RUN cp -r /code/stronka /usr/local/lib/python3.10/dist-packages
WORKDIR /code

CMD [ "python3", "app.py" ]
