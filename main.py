
import cv2
import numpy as np
import os
import shutil

from flask import Flask, render_template, request, redirect, url_for, send_from_directory


app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'

if os.path.exists("uploads"):
    shutil.rmtree('uploads')
os.makedirs('uploads')


def getcircle(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray, (11, 11), 0)
    
    edges = cv2.Canny(blur, 0, 150, apertureSize=3)

    try:
        cnt, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(cnt)):

            if cnt[i].shape[0] > 5:

                ellipse = cv2.fitEllipse(cnt[i])  # [(椭圆中心点x, 椭圆中心点y), (椭圆短轴a, 椭圆长轴b), 中心旋转角度angle]
                a = ellipse[1][0]
                b = ellipse[1][1]
                if (125 < a < 375 and b < 430) and (b / a < 2.1):
                    cv2.ellipse(img, ellipse, (0, 0, 255), 12)

        cv2.imencode('.jpg', img)[1].tofile(os.path.join("uploads", "标记.jpg"))

    except Exception as e:
        print(e)


@app.route('/')
def index():
    files = ['原图.jpg', '标记.jpg']
    return render_template('index.html', files=files)


@app.route('/', methods=['POST'])
def upload_files():
    upload_file = request.files['file']
    if upload_file.filename != '':
        if os.path.exists("uploads"):
            shutil.rmtree('uploads')
        os.makedirs('uploads')
        upload_file.save(os.path.join(app.config['UPLOAD_PATH'], "原图.jpg"))
        getcircle(os.path.join(app.config['UPLOAD_PATH'], "原图.jpg"))

    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


if __name__ == '__main__':
    app.run(debug=True)
