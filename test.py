
import cv2
import os


def getcircle(path):
    img = cv2.imread(path)  # 读取图片

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    edges = cv2.Canny(blur, 0, 150, apertureSize=3)

    try:
        cnt, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(cnt)):

            if cnt[i].shape[0] > 5:

                ellipse = cv2.fitEllipse(cnt[i])
                a = ellipse[1][0]
                b = ellipse[1][1]
                # if (100 < a < 375 and b < 410) and (b / a < 2):
                if (125 < a < 375 and b < 430) and (b / a < 2.1):
                    # print(a, b)
                    cv2.ellipse(img, ellipse, (0, 0, 255), 12)

        cv2.namedWindow("circle", 0)
        cv2.resizeWindow("circle", 640, 360)
        cv2.imshow('circle', img)
        cv2.waitKey(0)
        cv2.destroyWindow('circle')
    except Exception as e:
        print(e)


p = r'E:\Axle\imgs/'
for file in os.listdir(p):
    print(p + file)
    getcircle(os.path.join(p, file))
