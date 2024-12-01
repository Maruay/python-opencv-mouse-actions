import numpy as np
import argparse
import cv2 as cv
import mediapipe as mp
import pyautogui
from pynput.mouse import Button, Controller

screen_width, screen_height = pyautogui.size()
mouse = Controller()

# Util
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args

def get_angle(a, b, c):
    radians = np.arctan2(c[1]- b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return
    
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2 - x1, y2 - y1)
    return np.interp(L, [0, 1], [0, 1000])

#Action
def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip[0] * screen_width)
        y = int(index_finger_tip[1] * screen_height)
        pyautogui.moveTo(x, y)

def detect_gestures(image, landmark_list, results):
    if len(landmark_list) >= 21:
        index_finger_tip = landmark_list[8]
        index_middle_dist = get_distance((landmark_list[8], landmark_list[12]))
        index_ang = get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
        middle_ang = get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
        if (index_middle_dist < 50 and index_ang > 90):
            move_mouse(index_finger_tip)
        elif (index_ang < 50 and middle_ang > 90):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv.putText(image, 'Left Click', (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif (index_ang > 90 and middle_ang < 50):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv.putText(image, 'Right Click', (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif (index_ang < 50 and middle_ang < 50):
            pyautogui.doubleClick()
            cv.putText(image, 'Double Click', (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#Main
 
args = get_args()

cap_device = args.device
cap_width = args.width
cap_height = args.height

use_static_image_mode = args.use_static_image_mode
min_detection_confidence = args.min_detection_confidence
min_tracking_confidence = args.min_tracking_confidence

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

while True:
    # Process Key (ESC: end)
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break

    ret, image = cap.read()

    image = cv.flip(image, 1)  # Mirror display
    imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    landmark_list = []

    if results.multi_hand_landmarks is not None:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(image, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)

        for lm in hand_landmarks.landmark:
            landmark_list.append((lm.x, lm.y))
        
        detect_gestures(image, landmark_list, results)

    cv.imshow('Hand Gesture Recognition', image)

cap.release()
cv.destroyAllWindows()