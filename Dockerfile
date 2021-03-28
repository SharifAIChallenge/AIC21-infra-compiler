FROM reg.aichallenge.ir/python:3.8

RUN apt update && apt install -y vim curl gettext
WORKDIR /home
ADD ./requirements.txt ./requirements.txt
# ENV PIP_NO_CACHE_DIR 1
RUN pip install -r ./requirements.txt
ADD ./ ./
