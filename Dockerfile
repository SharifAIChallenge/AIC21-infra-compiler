FROM reg.aichallenge.ir/aic/base/infra/compiler:v4
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
RUN mkdir -p /var/log/compiler
WORKDIR /home/src
