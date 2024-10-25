from flask import Flask, send_file
import threading
import time
import json
from datetime import datetime
from Util import procTime, checkMoreThanSec
from ImageProc import ImageProc

app = Flask(__name__)
selectedPhotos = []
    
def update():
    global selectedPhotos
    selectedPhotos = list()

    with open('./vol/setting.json', 'r') as f:
        set = json.load(f)

    timeUP = set["start_time"]["update"]
    timePick = set["start_time"]["pick"]

    imgproc = ImageProc(set)
    
    imgproc.updateCpList()
    time.sleep(set["start_time"]["update"])
    
    swFirst = True
    lastUpdateTime = datetime.now()
    lastPickTime = datetime.now()

    while True:
        if checkMoreThanSec(lastUpdateTime, timeUP) or swFirst:
            swFirst = False
            imgproc.updateCpList()
            print(f"Update : {procTime(lastPickTime)}")
            lastUpdateTime = datetime.now()

        ret = imgproc.pathRandPick()
        for i in ret:
            selectedPhotos.append(i)

        while checkMoreThanSec(lastPickTime, timePick):
            time.sleep(10)
        print(f"Pick : {procTime(lastPickTime)}")
        lastPickTime = datetime.now()


t0 = threading.Thread(target=update)
t0.daemon = True
t0.start()

@app.route('/photo/<int:index>')
def photo(index):
    if 0 <= index < len(selectedPhotos):
        img = selectedPhotos[index]
        return send_file(img)
    else:
        return "Index out of range", 404

if __name__ == '__main__':
    app.run(debug=True)