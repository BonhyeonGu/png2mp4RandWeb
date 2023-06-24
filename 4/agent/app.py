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
    ret = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            ret.append(d)
            allDirs(d)
    return ret

def pickImageLocale(locale_inp, drop_distance, drop_step, pick_count=10, ):
    allDirsRet = allDirs(locale_inp)
    tempRet = []
    tempRetNoDel = []
    for dir in allDirsRet:
        if "@eaDir" in dir:#Synology bug
            continue
        dir2fileName_list = os.listdir(dir)
        for dir2fileName in dir2fileName_list:
            if dir2fileName.endswith(".png"):                
                tempRet.append((dir2fileName, dir+'/'+dir2fileName))
                tempRetNoDel.append((dir2fileName, dir+'/'+dir2fileName))

    try:
        with open('dropcache.txt','r') as f:
            drops = f.readlines()
    except FileNotFoundError:
        drops = []
    nextdrops = []
    for i in drops:
        i = i.split(',,,')
        i[1] = int(i[1])
        i[1] -= 1
        if i[1] > 0:
            nextdrops.append(i[0] + ',,,' + str(i[1]))
        for tuple in tempRet:
            if tuple[0] == i[0]:
                tempRet.remove(tuple)
                break
            
    ret = random.sample(tempRet, pick_count)

    for i in ret:
        for j, (x, _) in enumerate(tempRetNoDel):
            if x == i[0]:
                idx = j
        for j in range(drop_distance):
            pIdx = idx - (j+1)
            if pIdx < 0:
                break
            nextdrops.append(tempRetNoDel[pIdx][0] + ',,,' + str(drop_step))
        for j in range(drop_distance):
            pIdx = idx + (j+1)
            if pIdx > len(tempRetNoDel) - 1:
                break
            nextdrops.append(tempRetNoDel[pIdx][0] + ',,,' + str(drop_step))
        with open('dropcache.txt','w') as f:
            for i in range(len(nextdrops)):
                if i == len(nextdrops) - 1:
                    f.write(str(nextdrops[i]))
                else:
                    f.write(str(nextdrops[i]) + '\n')
    return ret

def resizeAndPutText(file_list, sw_tag, sw_date, w=1920, h=1080):
    global namePattern

    size = (w, h)
    for file in file_list:
        base_pic=np.zeros((size[1],size[0],3),np.uint8)
        pic1=cv2.imread(file[1], cv2.IMREAD_COLOR)
        try:
            while(True):
                h,w=pic1.shape[:2]
                break
        except:
            print("치명적인 문제!")
            print(file)
            continue
        ash = size[1]/h
        asw = size[0]/w
        if asw<ash:
            sizeas = (int(w*asw), int(h*asw))
        else:
            sizeas = (int(w*ash), int(h*ash))
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
    cmd += 'ffmpeg -loglevel fatal -y -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s ' % ("./" + file_list[0][0], "./" + file_list[1][0], "./" + file_list[2][0], "./" + file_list[3][0], "./" + file_list[4][0])
    cmd += ' -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s ' % ("./" + file_list[5][0], "./" + file_list[6][0], "./" + file_list[7][0], "./" + file_list[8][0], "./" + file_list[9][0])
    
    cmd += '-filter_complex "[0:v]fade=t=in:st=0:d=1, fade=t=out:st=9:d=1[v0]; '
    cmd += '[1:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v1]; [2:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v2]; '
    cmd += '[3:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v3]; [4:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v4]; '
    cmd += ' [5:v]fade=t=in:st=0:d=1, fade=t=out:st=9:d=1[v5]; '
    cmd += '[6:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v6]; [7:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v7]; '
    cmd += '[8:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v8]; [9:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v9]; '
    cmd += '[v0][v1][v2][v3][v4][v5][v6][v7][v8][v9]concat=n=10:v=1:a=0,format=yuv420p[v]" -map "[v]" %s' % ('./' + "out0.mp4")
    os.system(cmd)
    
def routine(locale_inp, drop_distance, drop_step, sftp_host, sftp_port, sftp_id, sftp_pw, remote_out, sw_tag, sw_date):
    print("%s start: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    file_list = pickImageLocale(locale_inp, drop_distance, drop_step,)
    for i in range(len(file_list)):
        print(file_list[i][1])
    resizeAndPutText(file_list, sw_tag, sw_date)
    #print("%s start: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    imagesToMp4(file_list)
    #print("%s end: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    os.system('rm -rf ./*.png')

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(sftp_host, port=sftp_port, username=sftp_id, password=sftp_pw, cnopts=cnopts) as sftp:
        sftp.put('./out0.mp4', remote_out+'out0.mp4')
    sftp.close()
    
    print("%s end: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("")

if __name__ == "__main__":
    with open('./locale.txt','r') as f:
        fs = f.read().split('\n')

        interTime = int(fs[0])
        locale_inp = fs[1]

        drop_distance = int(fs[2])
        drop_step = int(fs[3])
        
        t = fs[4].split(':')
        sftp_host = t[0]
        sftp_port = int(t[1])

        t = fs[5].split('/')
        sftp_id = t[0]
        sftp_pw = t[1]

        remote_out = fs[4]
        #/usr/share/nginx/html

        sw_tag = fs[6]
        sw_date = fs[7]

    while(True):
        sleep(interTime)
        if("START" in os.listdir('./cmd/')):
            routine(locale_inp, drop_distance, drop_step, sftp_host, sftp_port, sftp_id, sftp_pw, remote_out, sw_tag, sw_date)
