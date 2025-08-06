import cv2
import time
import math
from hand_tracking import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Webcam setup
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Pycaw setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range (in dB) and setup variables
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

volBar = 400
volPer = 0
pTime = 0
prevVolScalar = volume.GetMasterVolumeLevelScalar()  # Start from current system volume

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=True)

    if lmList:
        # Thumb tip = id 4, Index tip = id 8
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw points and line
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # Calculate distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Map length (20 to 200) to volume scalar (0.0 to 1.0)
        vol_scalar = (length - 20) / (200 - 20)
        vol_scalar = max(0.0, min(1.0, vol_scalar))  # Clamp between 0 and 1

        # Only update volume if change is significant (dead zone)
        if abs(prevVolScalar - vol_scalar) > 0.05:
            volume.SetMasterVolumeLevelScalar(vol_scalar, None)
            prevVolScalar = vol_scalar  # Update last volume

    # Get current system volume scalar (0.0–1.0)
    currentVol = volume.GetMasterVolumeLevelScalar()
    volPer = int(currentVol * 100)
    volBar = int(400 - volPer * 2.5)

    # Draw volume bar and percentage
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
    cv2.rectangle(img, (50, volBar), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{volPer} %', (40, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 3)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime + 1e-5)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (500, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Display image
    cv2.imshow("Gesture Volume Control", img)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
