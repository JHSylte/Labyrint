import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

RESOLUTION = (640, 480)
hsvVals = {'hmin': 0, 'smin': 164, 'vmin': 139, 'hmax': 179, 'smax': 255, 'vmax': 218}
centerPoint = (RESOLUTION[0] // 2, RESOLUTION[1] // 2, 1000)
myColorFinder = ColorFinder(False)

def init_camera():
    camera = cv2.VideoCapture(0)
    camera.set(3, RESOLUTION[0])
    camera.set(4, RESOLUTION[1])
    if not camera.isOpened():
        raise RuntimeError("Kamera kunne ikke åpnes.")
    return camera

camera = init_camera()

def get_ball_position():
    ret, img = camera.read()
    if not ret:
        return None

    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)
    cv2.imshow("Ballsporing", imgContour)
    cv2.waitKey(1)

    if contours:
        x = contours[0]['center'][0] - centerPoint[0]
        y = (RESOLUTION[1] - contours[0]['center'][1]) - centerPoint[1]
        z = (contours[0]['area'] - centerPoint[2]) / 1000
        return x, y, z
    return None
