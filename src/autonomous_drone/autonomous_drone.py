from djitellopy import Tello
from src.pose_detection.body import Body
from src.autonomous_drone.non_blocking_wait import NonBlockingWait
from typing import List, Tuple, Optional
import cv2

class AutonomousDrone:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.set_speed(10)
        self.tello.streamoff()
        self.tello.streamon()

        self.frame_read = self.tello.get_frame_read()

        first_frame = self.__resize_frame(self.get_frame())
        self.W = first_frame.shape[1]
        self.H = first_frame.shape[0]
        self.center_x = int(self.W/2)
        self.center_y = int(self.H/2)

        self.pose_model = Body('./res/model/body_pose_model.pth')

        self.wait = NonBlockingWait()
        self.SHOULD_RUN = True

    def takeoff(self):
        self.tello.takeoff()
        self.wait.wait_millis(3000)

    def get_frame(self):
        return self.frame_read.frame

    def __resize_frame(self, frame):
        scale_percent = 20  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def predict_pose(self, frame) -> List[Optional[Tuple[int, int]]]:
        keypoints_to_track = [0]
        keypoints = [None for i in range(len(keypoints_to_track))]
        candidate, subset = self.pose_model(frame)

        if len(subset) > 0:
            point_indexes = subset[0]  # Track only one person

            for idx, keypoint in enumerate(keypoints_to_track):
                point_idx = int(point_indexes[keypoint])
                if point_idx != -1:
                    x, y = candidate[point_idx][0:2]
                    keypoints[idx] = (int(x), int(y))
        return keypoints

    # Drone motor speeds between -100~100
    def calc_speeds(self, keypoints: List[Tuple]) -> List[int]:
        left_right = 0
        for_back = 0
        up_down = 0
        yaw = 0

        nose_keypoint = keypoints[0]
        if nose_keypoint is not None:
            nose_x, nose_y = nose_keypoint

            diff_x = (nose_x - self.center_x)/(self.W/2)
            diff_y = (self.center_y - nose_y)/(self.H/2)

            up_down = diff_y * 50


        return [int(left_right), int(for_back), int(up_down), int(yaw)]

    def update_motor_speeds(self, speeds: List[int]):
        self.tello.send_rc_control(speeds[0], speeds[1], speeds[2], speeds[3])

    def run(self, debug=False):
        self.takeoff()

        while self.SHOULD_RUN:
            frame = self.get_frame()
            frame = self.__resize_frame(frame)

            if self.wait.has_time_passed():
                keypoints = self.predict_pose(frame=frame)
                speeds = self.calc_speeds(keypoints=keypoints)
                self.update_motor_speeds(speeds=speeds)

                if debug:
                    for point in keypoints:
                        if point is not None:
                            cv2.circle(frame, (point[0], point[1]), 4, (253, 1, 36), thickness=-1)
                    cv2.circle(frame, (self.center_x, self.center_y), 4, (0, 0, 255), thickness=-1)

            cv2.imshow('Drone View', frame)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            elif k == ord('s'):
                print('>>> Taking off')
        # Stop the drone
        print('>>> Turning off drone')
        cv2.destroyAllWindows()
        self.tello.end()

    def stop(self):
        self.SHOULD_RUN = False

