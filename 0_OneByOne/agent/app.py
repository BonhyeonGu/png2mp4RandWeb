import json
from datetime import datetime
from time import sleep
import os
import numpy as np
import cv2
import random
import re

import pysftp


namePattern = re.compile("(\d\d\d\d)-(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d\d)")

def allDirs(rootdir: str, localeBlacks: list) -> list:
    ret = []
    for dir in os.listdir(rootdir):
        #포함 확인
        if any(black in dir for black in localeBlacks):
            continue
        d = os.path.join(rootdir, dir)
        if os.path.isdir(d):
            ret.append(d)
            ret += allDirs(d, localeBlacks)
    return ret

def pickImageLocale(localeInp: str, localeBlacks: list, dropD: int, dropS: int, pick_count=10):
    allDirsRet = allDirs(localeInp, localeBlacks)
    tempRet = []
    tempRetNoDel = []
    for dir in allDirsRet:
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
        for j in range(dropD):
            pIdx = idx - (j+1)
            if pIdx < 0:
                break
            nextdrops.append(tempRetNoDel[pIdx][0] + ',,,' + str(dropS))
        for j in range(dropD):
            pIdx = idx + (j+1)
            if pIdx > len(tempRetNoDel) - 1:
                break
            nextdrops.append(tempRetNoDel[pIdx][0] + ',,,' + str(dropS))
        with open('dropcache.txt','w') as f:
            for i in range(len(nextdrops)):
                if i == len(nextdrops) - 1:
                    f.write(str(nextdrops[i]))
                else:
                    f.write(str(nextdrops[i]) + '\n')
    return ret

def resizeAndPutText(fileList: list, tagOn: bool, dateType: int, localeTags: dict, w=1920, h=1080):
    global namePattern

    size = (w, h)
    for file in fileList:
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

        if tagOn:
            if dateType == 0:
                tag = os.path.getctime(file[1])
                timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            elif dateType == 1:
                tag = os.path.getmtime(file[1])
                timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            elif dateType == 2:
                search_res = namePattern.search(file[0])
                try:
                    search_res = search_res.groups()
                    timetag = '%s.%s.%s %s:%s'%(search_res[0], search_res[1], search_res[2], search_res[3], search_res[4])
                except:
                    tag = os.path.getmtime(file[1])
                    timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            else:
                break
            #------------------------------------------------------
            untagch = True
            for key in localeTags.keys():
                if key in file[1]:
                    timetag += f" {localeTags[key]}"
                    untagch = False
                    break
            if untagch:
                timetag += "__"
            #------------------------------------------------------
            cv2.putText(base_pic,timetag,(1528,1040),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,0,0),4,cv2.LINE_AA)
            cv2.putText(base_pic,timetag,(1528,1040),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
        cv2.imwrite('./' + file[0], base_pic)

def imagesToMp4(fileList):
    cmd = ""
    cmd += 'ffmpeg -loglevel fatal -y -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s ' % ("./" + fileList[0][0], "./" + fileList[1][0], "./" + fileList[2][0], "./" + fileList[3][0], "./" + fileList[4][0])
    cmd += ' -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s -loop 1 -t 10 -i %s ' % ("./" + fileList[5][0], "./" + fileList[6][0], "./" + fileList[7][0], "./" + fileList[8][0], "./" + fileList[9][0])
    
    cmd += '-filter_complex "[0:v]fade=t=in:st=0:d=1, fade=t=out:st=9:d=1[v0]; '
    cmd += '[1:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v1]; [2:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v2]; '
    cmd += '[3:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v3]; [4:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v4]; '
    cmd += ' [5:v]fade=t=in:st=0:d=1, fade=t=out:st=9:d=1[v5]; '
    cmd += '[6:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v6]; [7:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v7]; '
    cmd += '[8:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v8]; [9:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v9]; '
    cmd += '[v0][v1][v2][v3][v4][v5][v6][v7][v8][v9]concat=n=10:v=1:a=0,format=yuv420p[v]" -map "[v]" %s' % ('./' + "out0.mp4")
    os.system(cmd)
    
def routine(localeInp: str, localeBlacks: list, localeTags: dict, dropD: int, dropS: int, tagOn: bool, dateType: str, mp4On: bool, host: str, port: int, id: str, pw: str, sftpOutLocale: str, ) -> None:
    print("%s start: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    fileList = pickImageLocale(localeInp, localeBlacks, dropD, dropS)
    for i in range(len(fileList)):
        print(fileList[i][1])
    resizeAndPutText(fileList, tagOn, dateType, localeTags)

    #print("%s start: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    if mp4On:
        imagesToMp4(fileList)
    #print("%s end: ffmpeg" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    maxIdx = 0
    for idx, file in enumerate(fileList):
        os.rename(os.path.join("./", file[0]), os.path.join("./", f"{idx}.png"))
        maxIdx = idx
    #----------------------------------------------------------------------------------------------------------
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, port=port, username=id, password=pw, cnopts=cnopts) as sftp:
        for i in range(maxIdx + 1):
            sftp.put(f"./{i}.png", sftpOutLocale+f"{i}.png")
        if mp4On:
            sftp.put('./out0.mp4', sftpOutLocale+'out0.mp4')
    #----------------------------------------------------------------------------------------------------------
    os.system('rm -rf ./*.png')

    print("%s end: routine" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("")

if __name__ == "__main__":
    with open('./png2mp4.json', 'r') as f:
        inp = json.load(f)
        interTime = inp["interTime"]
        localeInp = inp["locale_inp"]
        localeBlacks = inp["locale_blacklist"]
        localeTags = inp["locale_tag"]

        tagOn = inp["tag_on"]
        dateType = inp["date_type"]
        mp4On = inp["mp4_on"]

        dropD = inp["drop"]["distance"]
        dropS = inp["drop"]["step"]
        host = inp["sftp"]["host"]
        port = inp["sftp"]["port"]
        id = inp["sftp"]["id"]
        pw = inp["sftp"]["pw"]
        sftpOutLocale = inp["sftp"]["locale"]

    while(True):
        sleep(interTime)
        if("START" in os.listdir('./cmd/')):
            routine(localeInp, localeBlacks, localeTags, dropD, dropS, tagOn, dateType, mp4On, host, port, id, pw, sftpOutLocale)
