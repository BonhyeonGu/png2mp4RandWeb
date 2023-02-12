from datetime import datetime
from time import sleep
import os
import numpy as np
import cv2
import random
import re

import pysftp


namePattern = re.compile("(\d\d\d\d)-(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d\d)")

allDirsRet = []
def allDirs(rootdir):
    global allDirsRet
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            allDirsRet.append(d)
            allDirs(d)

def pickImageLocale(locale_inp, pick_count=10):
    allDirs(locale_inp)
    global allDirsRet
    allDirsRet.append(locale_inp)
    #print(allDirsRet)

    dir_list = allDirsRet

    file_list = []
    for dir in dir_list:
        if "@eaDir" in dir:#Synology bug
            continue
        dir2fileName_list = os.listdir(dir)
        for dir2fileName in dir2fileName_list:
            if dir2fileName.endswith(".png"):
                file_list.append((dir2fileName, dir+'/'+dir2fileName))

    while(len(file_list) < pick_count):
        print("파일 개수가, 원하고자 하는 크기보다 적습니다!")
        file_list = []
        for dir in dir_list:
            if "@eaDir" in dir:
                continue
            dir2fileName_list = os.listdir(dir)
            for dir2fileName in dir2fileName_list:
                if dir2fileName.endswith(".png"):
                    file_list.append((dir2fileName, dir+'/'+dir2fileName))

    file_list = random.sample(file_list, pick_count)
    return file_list

def resizeAndPutText(file_list, sw_tag, sw_date, w=1920, h=1080):
    global namePattern

    size=(w, h)
    for file in file_list:
        base_pic=np.zeros((size[1],size[0],3),np.uint8)
        pic1=cv2.imread(file[1], cv2.IMREAD_COLOR)
        h,w=pic1.shape[:2]
        ash=size[1]/h
        asw=size[0]/w
        if asw<ash:
            sizeas=(int(w*asw), int(h*asw))
        else:
            sizeas=(int(w*ash), int(h*ash))
        pic1 = cv2.resize(pic1,dsize=sizeas)
        base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2),
        int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=pic1

        if sw_tag == '1':
            if sw_date == '0':
                tag = os.path.getctime(file[1])
                timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            elif sw_date == '1':
                tag = os.path.getmtime(file[1])
                timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            elif sw_date == '2':
                search_res = namePattern.search(file[0])
                try:
                    search_res = search_res.groups()
                    timetag = '%s.%s.%s %s:%s'%(search_res[0], search_res[1], search_res[2], search_res[3], search_res[4])
                except:
                    tag = os.path.getmtime(file[1])
                    timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            else:
                break
            cv2.putText(base_pic,timetag,(1585,1040),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,0,0),4,cv2.LINE_AA)
            cv2.putText(base_pic,timetag,(1585,1040),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
        cv2.imwrite('./' + file[0], base_pic)

def imagesToMp4(file_list):
    cmd = ""
    cmd += 'ffmpeg -y -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s ' % ("./" + file_list[0][0], "./" + file_list[1][0], "./" + file_list[2][0], "./" + file_list[3][0], "./" + file_list[4][0])
    cmd += ' -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s ' % ("./" + file_list[5][0], "./" + file_list[6][0], "./" + file_list[7][0], "./" + file_list[8][0], "./" + file_list[9][0])
    
    cmd += '-filter_complex "[0:v]fade=t=in:st=0:d=1, fade=t=out:st=9:d=1[v0]; '
    cmd += '[1:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v1]; [2:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v2]; '
    cmd += '[3:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v3]; [4:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v4]; '
    cmd += ' [5:v]fade=t=in:st=0:d=1, fade=t=out:st=9:d=1[v5]; '
    cmd += '[6:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v6]; [7:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v7]; '
    cmd += '[8:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v8]; [9:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v9]; '
    cmd += '[v0][v1][v2][v3][v4][v5][v6][v7][v8][v9]concat=n=10:v=1:a=0,format=yuv420p[v]" -map "[v]" %s' % ('./' + "out0.mp4")
    os.system(cmd)
    
def routine(locale_inp, sftp_host, sftp_port, sftp_id, sftp_pw, remote_out, sw_tag, sw_date):
    print("%s start: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    file_list = pickImageLocale(locale_inp)
    #print(file_list)
    resizeAndPutText(file_list, sw_tag, sw_date)
    print("%s start: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    imagesToMp4(file_list)
    print("%s end: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    os.system('rm -rf ./*.png')

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(sftp_host, port=sftp_port, username=sftp_id, password=sftp_pw, cnopts=cnopts) as sftp:
        sftp.put('./out0.mp4', remote_out+'out0.mp4')
    sftp.close()
    
    print("%s end: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == "__main__":
    with open('./locale.txt','r') as f:
        fs = f.read().split('\n')

        interTime = int(fs[0])
        locale_inp = fs[1]
        
        t = fs[2].split(':')
        sftp_host = t[0]
        sftp_port = int(t[1])

        t = fs[3].split('/')
        sftp_id = t[0]
        sftp_pw = t[1]

        remote_out = fs[4]
        #/usr/share/nginx/html

        sw_tag = fs[5]
        sw_date = fs[6]

    while(True):
        sleep(interTime)
        if("START" in os.listdir('./cmd/')):
            routine(locale_inp, sftp_host, sftp_port, sftp_id, sftp_pw, remote_out, sw_tag, sw_date)
