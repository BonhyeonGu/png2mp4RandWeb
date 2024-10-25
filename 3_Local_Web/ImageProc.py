import numpy as np
import cv2
import os
import re
from datetime import datetime
import random
import json

from Util import allFilesTwoList, allFilesSet 

class ImageProc:
    def __init__(self, dictArg: dict) -> None:
        self.namePattern = re.compile("(\d\d\d\d)-(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d\d)")

        self.pDirOri = dictArg['path']['dir_original']
        self.pDirCp = os.path.join(dictArg['path']['dir_volume'], 'cp')
        self.pFileCpList = os.path.join(dictArg['path']['dir_volume'], 'update_list.json')
        self.pFileDrop = os.path.join(dictArg['path']['dir_volume'], 'dropcache.json')
        
        self.dirBlack = dictArg['dirBlacklist']
        self.dropD = dictArg['drop']['distance']
        self.dropS = dictArg['drop']['step']
        self.numPick = dictArg['pick_num']
        self.oSizeW = dictArg['size']['width']
        self.oSizeH = dictArg['size']['height']
        self.oSizeTX = dictArg['size']['tx']
        self.oSizeTY = dictArg['size']['ty']

        self.tagSw = dictArg['tag']['sw']
        self.tagType = dictArg['tag']['type']
        self.pathToTag = dictArg['tag']['path_to_tag']
        
        if not os.path.exists(self.pDirCp):
            os.makedirs(self.pDirCp)

    
    def image_ReSize_PutText_Copy(self, fullName: str, tagOn: bool, dateType: int, localeTags: dict) -> None:
        name = os.path.basename(fullName)

        w = self.oSizeW
        h = self.oSizeH

        size = (w, h)

        base_pic=np.zeros((size[1],size[0],3),np.uint8)
        pic1=cv2.imread(fullName, cv2.IMREAD_COLOR)
        try:
            while(True):
                h,w=pic1.shape[:2]
                break
        except:
            print("치명적인 문제!")
            print(fullName)
            return
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
                tag = os.path.getctime(fullName)
                timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            elif dateType == 1:
                tag = os.path.getmtime(fullName)
                timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            elif dateType == 2:
                search_res = self.namePattern.search(name)
                try:
                    search_res = search_res.groups()
                    timetag = '%s.%s.%s %s:%s'%(search_res[0], search_res[1], search_res[2], search_res[3], search_res[4])
                except:
                    tag = os.path.getmtime(fullName)
                    timetag = datetime.fromtimestamp(tag).strftime('%Y.%m.%d %H:%M')
            else:
                return
            #------------------------------------------------------
            untagch = True
            for key in localeTags.keys():
                if key in fullName:
                    timetag += f" {localeTags[key]}"
                    untagch = False
                    break
            if untagch:
                timetag += "__"
            #------------------------------------------------------
            cv2.putText(base_pic,timetag,(self.oSizeTX,self.oSizeTY),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,0,0),4,cv2.LINE_AA)
            cv2.putText(base_pic,timetag,(self.oSizeTX,self.oSizeTY),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
        cv2.imwrite(os.path.join(self.pDirCp, name), base_pic)


    def updateCpList(self) -> None:
        cps = set()
        try:
            with open(self.pFileCpList, 'r') as f:
                for line in f:
                    file_name, file_size = line.strip().split(',')
                    cps.add((file_name, int(file_size)))
        except FileNotFoundError:
            pass
        
        oris = allFilesSet(self.pDirOri, self.dirBlack, 'png')

        cMo = cps - oris
        numDel = len(cMo)
        for fullName, size in cMo:
            os.system(f'rm -rf {fullName}')
            cps.remove((fullName, size))
        oMc = oris - cps
        numNew = len(oMc)
        for fullName, size in oMc:
            self.image_ReSize_PutText_Copy(fullName, self.tagSw, self.tagType, self.pathToTag)
            cps.add((fullName, size))

        with open(self.pFileCpList, 'w') as f:
            for item in cps:
                f.write(f"{item[0]},{item[1]}\n")

        print(f"Deleted : {numDel}, Created : {numNew}")


    def pathRandPick(self) -> list:
        #------------------------------------------------------------------------------------------
        tempRet, emmRet = allFilesTwoList(self.pDirCp, self.dirBlack, 'png')
        #------------------------------------------------------------------------------------------
        try:
            with open(self.pFileDrop, 'r') as f:
                dropFiles = json.load(f)
        except FileNotFoundError:
            dropFiles = dict()
        #------------------------------------------------------------------------------------------
        nextDropFiles = dict()
        #------------------------------------------------------------------------------------------
        tempRet = [item for item in tempRet if item not in dropFiles or dropFiles[item] <= 1]
        
        if len(tempRet) < self.numPick:
            print("!!! : Small Result, Please edit Distance or Step")
            nextDropFiles = dict()
            ret = random.sample(emmRet, self.numPick)
        else:
            idxList = list(range(len(tempRet)))
            idxRet = []
            ret = []
            # 위에는 키 값으로 비교하지만 여기선 인덱스로 비교한다. 순서가 꼬일 수 있다는 것을 고려해야한다.
            # 효율 없지만 순서가 지켜져야하기 때문에..
            for i in range(self.numPick):
                ri = random.choice(idxList)
                for j in range(ri, ri + self.dropD + 1):
                    if j in idxList:
                        idxList.remove(j)
                        nextDropFiles[tempRet[j]] = self.dropS
                for j in range(ri - self.dropD, ri):
                    if j in idxList:
                        idxList.remove(j)
                        nextDropFiles[tempRet[j]] = self.dropS
                idxRet.append(ri)
                #------------------------------------------------------------------------------------------
                # [0]은 이름 [1]은 파일 경로
                nextDropFiles[tempRet[ri]] = self.dropS
                ret.append(tempRet[ri])
            #------------------------------------------------------------------------------------------
            for key, value in dropFiles.items():
                if value > 1:
                    nextDropFiles[key] = value - 1
            
            with open(self.pFileDrop, 'w') as f:
                json.dump(nextDropFiles, f, indent=4)
            #------------------------------------------------------------------------------------------
        return ret
