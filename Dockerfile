FROM nginx
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y

#Time
RUN apt-get install -y git nano tzdata openssh-server tzdata python3 python3-pip
RUN apt install -y python3-opencv
RUN pip3 install -y numpy
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

WORKDIR /root
RUN git clone https://github.com/BonhyeonGu/png2mp4RandWeb p

WORKDIR /root/p
CMD [ "python3  ./app.py" ]