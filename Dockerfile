FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get install python3-pip -y
RUN apt install -y wget unzip
RUN apt-get install -y tzdata
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt -f install -y
RUN pip install -r requirements.txt
COPY . /code/
USER 1001

CMD [ "python3", "app.py" ]
