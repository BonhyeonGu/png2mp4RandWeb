FROM nginx
LABEL email="bonhyeon.gu@9bon.org"
LABEL name="BonhyeonGu"
ENV TZ=Asia/Seoul
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt update
RUN apt install -y ffmpeg

#Time-------------------------------------------------------
RUN apt-get install -y git tzdata python3 python3-pip
RUN apt install -y python3-opencv rclone
RUN pip3 install numpy pysftp
RUN echo $TZ > /etc/timezone && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean
#-----------------------------------------------------------

#SSH--------------------------------------------------------
RUN apt-get install -y openssh-server
RUN echo "PermitRootLogin yes \nPasswordAuthentication yes \nChallengeResponseAuthentication no" >> /etc/ssh/sshd_config
RUN echo "root:1234" | chpasswd
#-----------------------------------------------------------

WORKDIR /root
RUN git clone https://github.com/BonhyeonGu/png2mp4RandWeb p

WORKDIR /root/p/3/
COPY ./locale.txt ./
ENTRYPOINT ["/bin/sh", "-c" , "service ssh start && service nginx start && python3 app.py"]