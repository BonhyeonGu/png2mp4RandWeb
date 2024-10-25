from flask import Flask, send_from_directory, jsonify
import threading
import time
import json
from ImageProc import ImageProc

selectedPhotos = []

app = Flask(__name__)
    
def update():
    global selectedPhotos
    selectedPhotos = list()

    with open('./setting.json', 'r') as f:
        set = json.load(f)
    imgproc = ImageProc(set)

    imgproc.updateCpList()
    time.sleep(set["sleep"]["cp"])
    while True:
        ret = imgproc.pathRandPick()
        for i in ret:
            selectedPhotos.append(i)
        time.sleep(set["sleep"]["pick"])

t0 = threading.Thread(target=update)
t0.daemon = True
t0.start()

@app.route('/random-photos')
def random_photos():
    if selected_photos:
        # 선택된 N개의 파일을 JSON 형식으로 반환 (접근 가능)
        return jsonify(selected_photos)
    else:
        return "No photos found", 404

@app.route('/photo/<filename>')
def get_photo(filename):
    # 요청된 파일이 selected_photos에 있으면 제공
    if filename in selected_photos:
        return send_from_directory(PHOTO_DIR, filename)
    else:
        return "File not available", 404

if __name__ == '__main__':
    app.run(debug=True)