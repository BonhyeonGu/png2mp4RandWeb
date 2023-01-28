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

WORKDIR /root/p/2/agent
COPY ./locale.txt ./
ENTRYPOINT ["/bin/sh", "-c" , "rclone mount --config=/root/.config/rclone/rclone.conf --user-agent=sauberlich --umask=002 --gid=100 --uid=1000 --allow-other --timeout=1h - -poll-interval=10s --dir-cache-time=5000h --cache-dir/mnt/rclone/cache --drive-pacer-min-sleep 10ms --drive-pacer-burst 1000 --vfs-cache- mode=off --vfs-cache-max-size=1G --vfs-cache-max-age=5000h --vfs-cache-poll-interval 5m --vfs-read-ahead 2G nextcloud: /mnt/nextcloud/ date && service ssh start && service nginx start && python3 app.py"]