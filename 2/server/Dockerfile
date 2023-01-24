FROM nginx
LABEL email="bonhyeon.gu@9bon.org"
LABEL name="BonhyeonGu"
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt update

#Time-------------------------------------------------------
RUN apt-get install -y tzdata
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean
#-----------------------------------------------------------

#SSH--------------------------------------------------------
RUN apt-get install -y openssh-server
RUN echo "PermitRootLogin yes \nPasswordAuthentication yes \nChallengeResponseAuthentication no" >> /etc/ssh/sshd_config
RUN echo "root:!@@!@!@sd78S21DFfsd!!@@dsaas21d!!98DSFDS@O21O!!!@!!@" | chpasswd
#-----------------------------------------------------------

WORKDIR /root
RUN git clone https://github.com/BonhyeonGu/png2mp4RandWeb p

WORKDIR /root/p
COPY ./locale.txt ./
ENTRYPOINT ["/bin/sh", "-c" , "service ssh start && service nginx start && python3 app.py"]