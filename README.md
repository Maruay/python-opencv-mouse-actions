# Mouse actions using hand gesture recognition
Perform mouse actions (move, right click, left click double click) using hand gesture recognition.

## :star2: Description
This is computer vision program that detect hand landmarks using mediapipe to detemine the mouse action:
- Mouse Movement
- Left Click
- Right Click
- Double Click

## :flight_departure:	Getting Started
### :bangbang: Prerequisites
- [numpy](https://numpy.org/)
- [cv2](https://opencv.org/)
- [mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide)
- [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
- [pynput.mouse](https://pynput.readthedocs.io/en/latest/)

### :dart: Features
1. **Hand Gesture Recognition**

<img width="482" alt="image" src="https://github.com/user-attachments/assets/46d58113-9995-4b53-858b-162cc3ba3fc4">

First of all, I use open cv and mediapipe to detect hand landmarks. In mediapipe, there is a vision task called `Hand Landmark Detection` which detects the keypoint localization of 21 hand-knuckle coordinates within the detected hand regions.

<img width="535" alt="image" src="https://github.com/user-attachments/assets/2f80c64d-5e32-4374-a764-84962ecb4b07">

In this project, I only consider landmarks of index and middle fingers, therefore, the landmarks that I use are between landmark number 5 to 12.

3. **Mouse movement**
4. **Left click**
5. **Right click**
6. **Double click**
