from datetime import datetime
from time import sleep
import os
import numpy as np
import cv2
import random

allDirsRet = []
def allDirs(rootdir):
    global allDirsRet
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            allDirsRet.append(d)
            allDirs(d)

def pickImageLocale(locale_inp, pick_count=5):
    allDirs(locale_inp)
    global allDirsRet

    dir_list = allDirsRet
    file_list = []
    for dir in dir_list:
        if "@eaDir" in dir:#Synology bug
            continue
        dir2fileName_list = os.listdir(dir)
        for dir2fileName in dir2fileName_list:
            if dir2fileName.endswith(".png"):
                
                file_list.append((dir2fileName, dir+'/'+dir2fileName))

    file_list = random.sample(file_list, pick_count)
    return file_list

def resizeAndPutText(file_list, putName=True, w=1920, h=1080):
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

        if putName:
            ctime = datetime.fromtimestamp(os.path.getctime(file[1])).strftime('%Y.%m.%d %H:%M')
            cv2.putText(base_pic,ctime,(1585,1040),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,0,0),4,cv2.LINE_AA)
            cv2.putText(base_pic,ctime,(1585,1040),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
        cv2.imwrite('./' + file[0], base_pic)

def imagesToMp4(file_list):
    cmd = 'ffmpeg -y -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s -loop 1 -t 5 -i %s ' % ("./" + file_list[0][0], "./" + file_list[1][0], "./" + file_list[2][0], "./" + file_list[3][0], "./" + file_list[4][0])
    cmd += '-filter_complex "[0:v]fade=t=in:st=0:d=1, fade=t=out:st=4:d=1[v0]; '
    cmd += '[1:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v1]; [2:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v2]; '
    cmd += '[3:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v3]; [4:v]fade=t=in:st=0:d=1,fade=t=out:st=4:d=1[v4]; '
    cmd += '[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0,format=yuv420p[v]" -map "[v]" %s' % ('./' + "out0.mp4")
    os.system(cmd)
    
def routine(locale_inp, locale_out):
    print("%s start: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    file_list = pickImageLocale(locale_inp)#!
    print(file_list)
    resizeAndPutText(file_list)#!
    print("%s start: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    imagesToMp4(file_list)#!
    print("%s end: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    os.system('rm -rf ./*.png')
    os.system('cp ./out0.mp4 %s' % (locale_out))
    print("%s end: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

if __name__ == "__main__":
    with open('./locale.txt','r') as f:
        fs = f.read().split('\n')
        interTime = int(fs[0])
        locale_inp = fs[1]
        locale_out = fs[2]
        #/usr/share/nginx/html
    routine(locale_inp, locale_out)

    flag = True
    while(True):
        if(int(datetime.now().hour) == 5 and flag):
            routine(locale_inp, locale_out)
            flag = False
        else:
            flag = True
        sleep(interTime)
        if("SKIP" in os.listdir('./cmd/')):
            routine(locale_inp, locale_out)
        if("SKIPONLYONE" in os.listdir('./cmd/')):
            routine(locale_inp, locale_out)
            os.system('rm ./cmd/SKIPONLYONE')

