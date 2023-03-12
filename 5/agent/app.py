from datetime import datetime
from time import sleep
import numpy as np
import os
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

def pickImageLocale(locale_inp, pick_count, sw_size):
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
                dir2fullName = dir + '/' + dir2fileName
                img = cv2.imread(dir2fullName, cv2.IMREAD_COLOR)
                h, w, c = img.shape
                if sw_size == '1' and h < w:
                    break
                elif sw_size == '2' and h > w:
                    break
                file_list.append((dir2fileName, dir2fullName))

    file_list = random.sample(file_list, pick_count)
    return file_list

def resizeAndPutText(file_list, sw_tag, sw_date, w, h, remote_out, output_names):
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
        cv2.imwrite('./' + output_names[0], base_pic)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(sftp_host, port=sftp_port, username=sftp_id, password=sftp_pw, cnopts=cnopts) as sftp:
            sftp.put('./' + output_names[0], remote_out + output_names[0])
        sftp.close()

def routine(locale_inp, remote_out, sw_tag, sw_date, sw_size, w, h, output_names):
    pick_count = len(output_names)
    file_list = pickImageLocale(locale_inp, pick_count, sw_size)#!
    print(file_list)
    resizeAndPutText(file_list, sw_tag, sw_date, w, h, remote_out, output_names)#!

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
        if("START" in os.listdir('./cmd/')):
            routine(locale_inp, remote_out, sw_tag, sw_date, '0', 1920, 1080, ["1.png", "2.png", "3.png", "4.png", "5.png"])
        sleep(interTime)

