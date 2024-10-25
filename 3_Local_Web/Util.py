from typing import List, Tuple
import os
from datetime import datetime


def procTime(start_time) -> str:
    now = datetime.now()
    elapsed_time = now - start_time
    formatted_time = str(elapsed_time).split('.')[0]  # 소수점 이하 제거
    return f"{formatted_time}"


def checkMoreThanSec(start_time, sec: int) -> bool:
    now = datetime.now()
    elapsed_seconds = (now - start_time).total_seconds()
    
    if elapsed_seconds > sec:
        return True
    else:
        return False


def allDirs(rootdir: str, localeBlacks: list) -> list:
    ret = []
    for dir in os.listdir(rootdir):
        if any(black in dir for black in localeBlacks):
            continue
        d = os.path.join(rootdir, dir)
        if os.path.isdir(d):
            ret.append(d)
            ret += allDirs(d, localeBlacks)
    return ret


def allFilesTwoList(rootdir: str, localeBlacks: list, ext: str) -> Tuple[List[str], List[str]]:
    allDirsRet = allDirs(rootdir, localeBlacks)
    allDirsRet.append(rootdir)
    ret0 = []
    ret1 = []
    #------------------------------------------------------------------------------------------
    for dir in allDirsRet:
        dir2fileName_list = os.listdir(dir)
        for dir2fileName in dir2fileName_list:
            # ext가 비어있으면 모든 파일을 수집, 아니면 확장자를 체크
            if not ext or dir2fileName.lower().endswith(ext):
                fullName = os.path.join(dir, dir2fileName)
                ret0.append(fullName)
                ret1.append(fullName)
    return ret0, ret1

def allFilesSet(rootdir: str, localeBlacks: list, ext: str):
    allDirsRet = allDirs(rootdir, localeBlacks)
    allDirsRet.append(rootdir)
    ret = set()
    #------------------------------------------------------------------------------------------
    for dir in allDirsRet:
        dir2fileName_list = os.listdir(dir)
        for dir2fileName in dir2fileName_list:
            # ext가 비어있으면 모든 파일을 수집, 아니면 확장자를 체크
            if not ext or dir2fileName.lower().endswith(ext):
                fullName = os.path.join(dir, dir2fileName)
                ret.add((fullName, os.path.getsize(fullName)))
    return ret