from flask import Flask, send_file
import threading
import time
import json
from datetime import datetime
from Util import procTime, checkMoreThanSec
from ImageProc import ImageProc
import logging


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

selectedPhotos = []
    
def update():
    global selectedPhotos

    with open('/vol/setting.json', 'r') as f:
        set = json.load(f)

    timeUP = set["start_time"]["update"]
    timePick = set["start_time"]["pick"]
    imgproc = ImageProc(set)
    
    swFirst = True
    lastUpdateTime = datetime.now()
    lastPickTime = datetime.now()

    print('SUB -- Start Daemon')
    while True:
        # Update check
        if checkMoreThanSec(lastUpdateTime, timeUP) or swFirst:
            tTime = datetime.now()
            imgproc.updateCpList()
            print(f" >> {procTime(tTime)}")
            lastUpdateTime = datetime.now()

        # Pick check
        if checkMoreThanSec(lastPickTime, timePick) or swFirst:
            swFirst = False
            tTime = datetime.now()
            ret = imgproc.pathRandPick()
            selectedPhotos = list()
            for i in ret:
                selectedPhotos.append(i)
            print(f"SUB -- {tTime}--> Picked >> {procTime(tTime)}")
            lastPickTime = datetime.now()

        time.sleep(5)


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
    app.run(host='0.0.0.0', debug=False)