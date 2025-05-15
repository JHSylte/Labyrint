import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

def initTracker(camera_port, hsvOne, hsvTwo, show_window=True, resolution=(640, 480)):
    
    cap = cv2.VideoCapture(camera_port)

    cap.set(3, resolution[0])
    cap.set(4, resolution[1])
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)

    tracker = {
        'cap': cap,
        'color1': ColorFinder(False),
        'color2': ColorFinder(False),
        'hsv1': hsvOne,
        'hsv2': hsvTwo,
        'show': show_window,
        'res': resolution,
        'center': (resolution[0] // 2, resolution[1] // 2, 1000)
    }

    return tracker

def readPositions(tracker):
    cap = tracker['cap']
    ret, img = cap.read()
    if not ret:
        print("Feil ved lesing av bilde")
        cap.release()
        if tracker['show']:
            cv2.destroyAllWindows()
        return None

    img = cv2.GaussianBlur(img, (7, 7), 0)
    displayImg = img.copy()
    center = tracker['center']
    positions = []

    # Farge 1 – én ball
    _, mask1 = tracker['color1'].update(img.copy(), tracker['hsv1'])
    _, contours1 = cvzone.findContours(img.copy(), mask1, minArea=100)

    if contours1:
        c = contours1[0]
        x = c['center'][0] - center[0]
        y = (tracker['res'][1] - c['center'][1]) - center[1]
        z = (c['area'] - center[2]) / 1000
        positions.append(('farge1', x, y, z))
        if tracker['show']:
            cv2.circle(displayImg, c['center'], 10, (0, 255, 0), -1)
            cv2.putText(displayImg, f"1: X={x}, Y={y}, Z={z:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        positions.append(('farge1', None, None, None))

    # Farge 2 – to baller
    _, mask2 = tracker['color2'].update(img.copy(), tracker['hsv2'])
    _, contours2 = cvzone.findContours(img.copy(), mask2, minArea=100)

    if contours2:
        sortedContours = sorted(contours2, key=lambda c: c['area'], reverse=True)[:2]
        for i, c in enumerate(sortedContours):
            x = c['center'][0] - center[0]
            y = (tracker['res'][1] - c['center'][1]) - center[1]
            z = (c['area'] - center[2]) / 1000
            positions.append((f'farge2_{i+1}', x, y, z))
            if tracker['show']:
                cv2.circle(displayImg, c['center'], 10, (255, 0, 0), -1)
                cv2.putText(displayImg, f"2.{i+1}: X={x}, Y={y}, Z={z:.1f}",
                            (10, 60 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    else:
        positions.append(('farge2_1', None, None, None))
        positions.append(('farge2_2', None, None, None))

    if tracker['show']:
        cv2.imshow("Sporing", displayImg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

    return positions
