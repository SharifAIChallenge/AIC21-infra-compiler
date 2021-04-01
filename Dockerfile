FROM reg.aichallenge.ir/python:3.8

RUN apt update && apt install -y vim curl gettext
RUN apt-get update && \
apt install -y vim curl gettext cmake unzip && \
pip3 install pyinstaller

# install code
WORKDIR /home
ADD ./requirements.txt ./requirements.txt
# ENV PIP_NO_CACHE_DIR 1
RUN pip install -r ./requirements.txt

ADD ./src ./src
ADD ./scripts ./scripts

RUN chmod +x scripts/compile.sh
RUN chmod +x src/compiler-psudo.sh


# make logging directory
RUN mkdir -p /var/log/compier
WORKDIR /home/src
