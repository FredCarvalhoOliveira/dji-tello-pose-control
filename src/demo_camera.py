import cv2
import copy
import torch
from djitellopy import Tello
from src.pose_detection.body import Body

body_estimation = Body('../res/model/body_pose_model.pth')

print(f"Torch device: {torch.cuda.get_device_name()}")

send_rc_control = False

tello = Tello()
tello.connect()
tello.set_speed(10)
tello.streamoff()
tello.streamon()

cap = cv2.VideoCapture(1)
cap.set(3, 160)
cap.set(4, 120)
while True:
    ret, oriImg = cap.read()
    candidate, subset = body_estimation(oriImg)
    canvas = copy.deepcopy(oriImg)
    # NOSE 0
    # CHEST 1

    center_x = int(oriImg.shape[1]/2)
    center_y = int(oriImg.shape[0]/2)

    for i in [0]:
        for n in range(len(subset)):
        # for n in [0]:
            index = int(subset[n][i])
            # POINT NOT FOUND
            if index == -1:
                continue
            x, y = candidate[index][0:2]
            cv2.circle(canvas, (int(x), int(y)), 4, (253, 1, 36), thickness=-1)
            cv2.circle(canvas, (int(center_x), int(center_y)), 4, (0, 0, 255), thickness=-1)

            diff_x = (x - center_x)/(oriImg.shape[1]/2)
            diff_y = (center_y - y)/(oriImg.shape[0]/2)
            print(diff_y)

    cv2.imshow('demo', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

