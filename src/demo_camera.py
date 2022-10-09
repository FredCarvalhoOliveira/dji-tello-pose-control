import cv2
import copy
import torch
from djitellopy import Tello
from src.pose_detection.body import Body
from src.utils.utils import normalize_points
from src.utils.visual_debugger import VisualDebugger
from src.utils.utils import resize


def predict_pose(model, img):
    keypoints_to_track = [16, 17]
    keypoints = [None for i in range(len(keypoints_to_track))]
    candidate, subset = model(img)

    if len(subset) > 0:
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

while True:
    ret, oriImg = cap.read()

    resized = resize(oriImg, width=100)
    # NOSE 0
    # CHEST 1
    # RIGHT SHOULDER 2
    # RIGHT ELBOW 3
    # RIGHT HAND 4
    # LEFT SHOULDER 5
    # LEFT ELBOW 6
    # LEFT HAND 7
    # RIGHT HIP 8
    # RIGHT KNEE 9
    # RIGHT FOOT 10
    # LEFT HIP 11
    # LEFT KNEE 12
    # LEFT FOOT 13
    # RIGHT EYE 14
    # LEFT EYE 15
    # RIGHT EAR 16
    # LEFT EAR 17

    points = predict_pose(body_estimation, resized)
    norm_points = normalize_points(points, resized)

    debug_frame = oriImg.copy()
    # debug_frame = VisualDebugger.draw_offsets(debug_frame, ref_point=(0.5, 0.5), points=norm_points)
    debug_frame = VisualDebugger.draw_keypoints(debug_frame, norm_points)

    cv2.imshow('demo', debug_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

