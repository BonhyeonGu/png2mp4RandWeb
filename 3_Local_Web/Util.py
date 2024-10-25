from typing import List, Tuple
import os



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