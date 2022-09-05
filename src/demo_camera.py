import cv2
import copy
import torch
from djitellopy import Tello
from src.pose_detection.body import Body


def __resize_frame(self, frame):
    scale_percent = 20  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def predict_pose(model, img):
    keypoints_to_track = [0]
    keypoints = [None for i in range(len(keypoints_to_track))]
    candidate, subset = model(img)

    point_indexes = subset[0]  # Track only one person

    for idx, keypoint in enumerate(keypoints_to_track):
        point_idx = int(point_indexes[keypoint])
        if point_idx != -1:
            x, y = candidate[point_idx][0:2]
            keypoints[idx] = (int(x), int(y))
    return keypoints

body_estimation = Body('../res/model/body_pose_model.pth')

print(f"Torch device: {torch.cuda.get_device_name()}")

cap = cv2.VideoCapture(1)
cap.set(3, 160)
cap.set(4, 120)
while True:
    ret, oriImg = cap.read()
    # candidate, subset = body_estimation(oriImg)
    # canvas = copy.deepcopy(oriImg)
    # # NOSE 0
    # # CHEST 1
    #
    # center_x = int(oriImg.shape[1]/2)
    # center_y = int(oriImg.shape[0]/2)
    #
    # print(subset.shape)
    # print(subset)
    # print(subset[0][0])

    points = predict_pose(body_estimation, oriImg)
    print(points)

    for point in points:
        if point is not None:
            cv2.circle(canvas, (point[0], point[1]), 4, (253, 1, 36), thickness=-1)

    # cv2.circle(canvas, (int(center_x), int(center_y)), 4, (0, 0, 255), thickness=-1)

    # for i in [0]:
    #     for n in range(len(subset)):
    #     # for n in [0]:
    #         index = int(subset[n][i])
    #         # POINT NOT FOUND
    #         if index == -1:
    #             continue
    #         x, y = candidate[index][0:2]
    #         cv2.circle(canvas, (int(x), int(y)), 4, (253, 1, 36), thickness=-1)
    #         cv2.circle(canvas, (int(center_x), int(center_y)), 4, (0, 0, 255), thickness=-1)
    #
    #         diff_x = (x - center_x)/(oriImg.shape[1]/2)
    #         diff_y = (center_y - y)/(oriImg.shape[0]/2)

    cv2.imshow('demo', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

