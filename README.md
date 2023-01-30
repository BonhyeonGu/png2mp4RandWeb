# png2mp4RandWeb

## 프로젝트 설명

이미지 URL로 이미지를 불러올 수 없고 비디오 URL만 가능한 곳에서 서버에 저장된 이미지를 무작위로 표시하기 위해 만든 프로젝트입니다.

1. 디렉토리 (하위 디렉토리 포함)에서 무작위 png 파일을 5개 복사
2. 복사한 png 파일을 [OpenCV](https://opencv.org/)로 일괄 1920 \* 1080으로 변환한 뒤 파일의 생성된 날짜와 시간을 우측 하단에 삽입
3. 변환을 거친 png 파일을 [FFmpeg](https://ffmpeg.org/)(로 페이드인, 페이드아웃 효과를 넣고 out0.mp4로 생성
4. - 1번, 3번 프로젝트는 locale.txt에 지정된 위치로 생성된 out0.mp4를 복사 <br>
   - 2번, 4번 프로젝트는 sftp로 locale.txt 파일에 지정된 서버로 out0.mp4를 전송

## Docker-Compose

```
version: "3"
services:
  png2mp4_agent:
    tty: true
    stdin_open: true
    container_name: png2mp4_agent
    build:
      context: .
      dockerfile: ./Dockerfile
    ports:
      - "12000:22" # SSH Port
    volumes:
      - (사진 디렉토리):/source:ro
      - (SKIP 파일 생성 위치):/root/p/1/cmd
       # 2. /root/p/2/agent/cmd
       # 3. /root/p/3/cmd
       # 4. /root/p/4/agent/cmd
    environment:
      TZ: "Asia/Seoul"
```

- 프로젝트 디렉토리내에 docker-compose.yml 파일이 있습니다

## locale.txt

### 1번, 3번

```
600 #600초마다 반복
/source #이미지 디렉토리
/usr/share/nginx/html/ #out4.mp4를 복사할 위치
1 # 날짜와 시간 표시 : 0 = 끔, 1 = 켬
0 # 날짜와 시간 표시 기준 : 0 = 파일 생성 기준, 1 = 파일 수정 기준
```

### 2번, 4번

```
600 #600초마다 반복
/source #이미지 디렉토리
server_address:ssh_port #sftp 서버 접속 주소 및 포트
root/password #sftp 서버 계정
/usr/share/nginx/html/ #sftp로 out0.mp4를 전송할 디렉토리
1 # 날짜와 시간 표시 : 0 = 끔, 1 = 켬
0 # 날짜와 시간 표시 기준 : 0 = 파일 생성 기준, 1 = 파일 수정 기준
```

- locale.txt 파일 수정시 도커 이미지를 새로 빌드해야됩니다.

```
sudo docker-compose build --no-cache
```

## 사용법

### 1번~2번

별다른 추가 작업없이 바로 영상을 생성합니다.

#### SKIP

이 프로젝트는 locale.txt 파일에서 설정한 초마다 05시를 확인하는 반복문이 있습니다.

05시가 되기 전에 새로운 영상을 생성하고 싶으면

1. /root/p/1/cmd
2. /root/p/2/agent/cmd

- 사용하는 프로젝트에 따라서 디렉토리가 다릅니다.

해당 위치에 SKIP 또는 SKIPONLYONE 이름의 파일이 있으면 새로운 영상을 생성합니다.

```
1. # touch /root/p/1/cmd/SKIP
2. # touch /root/p/2/agent/cmd/SKIPONLYONE
```

### 3번~4번

Rclone으로 사용하는걸 상정하고 작업된 프로젝트입니다.

#### START

이 프로젝트는 locale.txt 파일에서 설정한 초마다 cmd 디렉토리내에 START를 확인하는 반복문이 있습니다.

3. /root/p/3/cmd
4. /root/p/4/agent/cmd

Rclone config로 Rclone을 설정한 후 사용하시는 프로젝트 번호내에 있는 cmd 디렉토리내에 START 파일을 생성해주면 영상을 생성하기 시작합니다.

```
3. # touch /root/p/3/cmd/START
4. # touch /root/p/4/agent/cmd/START
```

## 단축어

애플 기기에 있는 단축어 앱으로 간단하게 할 수 있습니다.

![Shortcut](/Shortcut.jpg)
