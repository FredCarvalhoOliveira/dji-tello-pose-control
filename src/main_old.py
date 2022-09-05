import cv2
import copy
import torch
from djitellopy import Tello
from src.pose_detection.body import Body
import time
import numpy as np

# body_estimation = Body('../res/model/body_pose_model.pth')
#
# print(f"Torch device: {torch.cuda.get_device_name()}")
#
# send_rc_control = False
#
# tello = Tello()
# tello.connect()
# tello.set_video_direction(tello.CAMERA_DOWNWARD)
# tello.set_speed(10)
# tello.streamoff()
# tello.streamon()
#
#
# frame_read = tello.get_frame_read()
#


while True:
    # frame = frame_read.frame
    # scale_percent = 20  # percent of original size
    # width = int(frame.shape[1] * scale_percent / 100)
    # height = int(frame.shape[0] * scale_percent / 100)
    # dim = (width, height)
    #
    # # resize image
    # frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    # print(frame.shape)
    #
    # candidate, subset = body_estimation(frame)
    # # canvas = copy.deepcopy(frame)
    # # # NOSE 0
    # # # CHEST 1
    # #
    # center_x = int(frame.shape[1]/2)
    # center_y = int(frame.shape[0]/2)
    #
    # for i in [0]:
    #     for n in range(len(subset)):
    #     # for n in [0]:
    #         index = int(subset[n][i])
    #         # POINT NOT FOUND
    #         if index == -1:
    #             continue
    #         x, y = candidate[index][0:2]
    #         cv2.circle(frame, (int(x), int(y)), 4, (253, 1, 36), thickness=-1)
    #         cv2.circle(frame, (int(center_x), int(center_y)), 4, (0, 0, 255), thickness=-1)
    #
    #         diff_x = (x - center_x)/(frame.shape[1]/2)
    #         diff_y = (center_y - y)/(frame.shape[0]/2)
    #         print(diff_y)
    #
    # cv2.imshow('demo', frame)
    cv2.imshow('demo', np.zeros((100, 100)))
    k = cv2.waitKey(1)
    if k == ord('q'):
        print('hdsuahduhsaduhsa')
        # break
    elif k == ord('s'):
        print('>>> Start take off')


# cap.release()
tello.streamoff()
tello.end()
cv2.destroyAllWindows()

