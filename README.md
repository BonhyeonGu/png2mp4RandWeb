<div align="center">

<h1>png2mp4</h1>

![d](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=FFFFFF) ![d](https://img.shields.io/badge/-Ffmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=FFFFFF)  

</div>

## 프로젝트 설명

여러 이미지중 5개를 무작위 선정하여 슬라이드 쇼 영상 형태로 만든 후 웹에 올리는 프로젝트입니다.
사진 전부를 전송할 수 없으나 무작위로 출력하고 싶은 환경에서 적합합니다.

프로젝트 디렉토리내 선택지 이후 docker-compose.yml를 사용할 수 있습니다.
dockerfile과 동일한 경로에 locale.txt를 만들어주어야 동작합니다.

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

- locale.txt 파일 수정시 도커 이미지를 새로 빌드해야하며, 실제 파일 내에는 주석이 없어야 합니다.

```Bash
sudo docker-compose build --no-cache
```

## 사용법

### 1번~2번

<div align="center">
<img width="479" alt="111" src="https://user-images.githubusercontent.com/24387014/215393679-bfa68d38-4b7a-4725-a19e-e4f0feb864bb.PNG">

이미지가 해당 agent 내에 존재할 때 적합합니다.

</div>

#### SKIP

이 프로젝트는 locale.txt 파일에서 설정한 초마다 05시를 확인하는 반복문이 있습니다.

05시가 되기 전에 새로운 영상을 생성하고 싶으면

1번의 경우 /root/p/1/cmd
2번의 경우 /root/p/2/agent/cmd

해당 위치에 SKIP 또는 SKIPONLYONE 이름의 파일이 있으면 새로운 영상을 생성합니다.

```
1. # touch /root/p/1/cmd/SKIP
2. # touch /root/p/2/agent/cmd/SKIPONLYONE
```

### 3번~4번

<div align="center">
<img width="490" alt="222" src="https://user-images.githubusercontent.com/24387014/215394654-4de24b82-b682-4b14-8664-cb5d7358787a.PNG">

Rclone으로 이미지 위치를 원격 마운트하여 불러오고 싶을 때 적합한 프로젝트입니다.

</div>

#### START

이 프로젝트는 locale.txt 파일에서 설정한 초마다 cmd 디렉토리내에 START를 확인하는 반복문이 있습니다.

3. /root/p/3/cmd
4. /root/p/4/agent/cmd

Rclone config로 Rclone을 설정한 후 사용하시는 프로젝트 번호내에 있는 cmd 디렉토리내에  
START 파일을 생성해주면 영상을 생성하기 시작합니다.

```
3. # touch /root/p/3/cmd/START
4. # touch /root/p/4/agent/cmd/START
```

## 단축어

아래는 애플의 단축어 앱 예제입니다.

<img width="490" alt="222" src="https://user-images.githubusercontent.com/24387014/215395214-4d82f9a3-8707-4435-862d-b757d2c767d8.jpg">

## Thanks for

<div align="center">
<img width="187" alt="5ignal" src="https://user-images.githubusercontent.com/24387014/215395620-652711ea-fc93-43c4-b366-d65f17c4f634.PNG">

[5ignal](https://github.com/5ignal)

</div>
