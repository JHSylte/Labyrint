import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

# Konfigurasjon
RESOLUTION = (640, 480)
HSV_VALS = {'hmin': 114, 'smin': 80, 'vmin': 130, 'hmax': 179, 'smax': 238, 'vmax': 255}
CENTER_POINT = (RESOLUTION[0] // 2, RESOLUTION[1] // 2, 1000)

# Initialiser fargesøker
colorFinder = ColorFinder(False)

# Globalt kameraobjekt
camera = None

def init_camera(camera_id=0, resolution=RESOLUTION):
    global camera
    if camera is not None:
        return  # Kamera er allerede initialisert
    cam = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cam.set(3, resolution[0])
    cam.set(4, resolution[1])
    if not cam.isOpened():
        raise RuntimeError(f"Kamera på port {camera_id} kunne ikke åpnes.")
    camera = cam

# Kalles automatisk ved import
init_camera()

def get_ball_position(show=False):
    """
    Returnerer (x, y, z) for ballposisjon, eller None hvis ingen ball funnet.
    """
    if camera is None:
        raise RuntimeError("Kamera ikke initialisert.")

    ret, frame = camera.read()
    if not ret:
        return None

    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    imgColor, mask = colorFinder.update(frame, HSV_VALS)
    imgContour, contours = cvzone.findContours(frame, mask, minArea=100)

    #if show:
    #    cv2.imshow("Ballsporing", imgContour)
    #    cv2.imshow("Mask", mask)
    #    cv2.waitKey(1)

    if contours:
        x = contours[0]['center'][0] - CENTER_POINT[0]
        y = (RESOLUTION[1] - contours[0]['center'][1]) - CENTER_POINT[1]
        z = (contours[0]['area'] - CENTER_POINT[2]) / 1000
        return x, y, z

    return None
