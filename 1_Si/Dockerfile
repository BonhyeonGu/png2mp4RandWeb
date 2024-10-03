FROM ubuntu:20.04
LABEL email="bonhyeon.gu@9bon.org"
LABEL name="BonhyeonGu"
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt update

RUN apt-get install -y git tzdata python3 python3-pip nano
RUN apt install -y python3-opencv cron
RUN pip3 install numpy
#Time-------------------------------------------------------
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean
#-----------------------------------------------------------

WORKDIR /root
RUN git clone https://github.com/BonhyeonGu/png2mp4RandWeb p

WORKDIR /root/p/1_Si
RUN mkdir cmd
RUN mkdir /source
COPY ./png2mp4.json ./
ENTRYPOINT ["/bin/sh", "-c" , "python3 app.py"]