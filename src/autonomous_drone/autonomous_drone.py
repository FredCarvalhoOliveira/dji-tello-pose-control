from djitellopy import Tello
from src.pose_detection.body import Body
from src.utils.non_blocking_wait import NonBlockingWait
from src.utils.utils import normalize_points, resize
from src.utils.visual_debugger import VisualDebugger
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

        self.center = (0.5, 0.5)

        self.pose_model = Body('./res/model/body_pose_model.pth')

        self.wait = NonBlockingWait()
        self.SHOULD_RUN = True

    def takeoff(self):
        self.tello.takeoff()
        self.wait.wait_millis(3000)

    def get_frame(self):
        return self.frame_read.frame

    def predict_pose(self, frame) -> List[Optional[Tuple[float, float]]]:
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
        return normalize_points(points=keypoints, frame=frame)

    # Drone motor speeds between -100~100
    def calc_speeds(self, keypoints: List[Optional[Tuple[float, float]]]) -> List[int]:
        left_right = 0
        for_back = 0
        up_down = 0
        yaw = 0

        nose_keypoint = keypoints[0]
        if nose_keypoint is not None:
            nose_x, nose_y = nose_keypoint

            diff_x = nose_x - self.center[0]
            diff_y = self.center[1] - nose_y

            left_right = diff_x * 40
            up_down = diff_y * 60

        return [int(left_right), int(for_back), int(up_down), int(yaw)]

    def update_motor_speeds(self, speeds: List[int]):
        self.tello.send_rc_control(speeds[0], speeds[1], speeds[2], speeds[3])

    def run(self, debug=False):
        self.takeoff()

        while self.SHOULD_RUN:
            original_frame = self.get_frame()
            frame = resize(original_frame, width=160)
            debug_frame = original_frame.copy()

            if self.wait.has_time_passed():
                keypoints = self.predict_pose(frame=frame)
                speeds = self.calc_speeds(keypoints=keypoints)
                self.update_motor_speeds(speeds=speeds)

                if debug:
                    debug_frame = VisualDebugger.draw_offsets(debug_frame, ref_point=(0.5, 0.5), points=keypoints)
                    debug_frame = VisualDebugger.draw_keypoints(debug_frame, keypoints)

                    text = "Battery: {}%".format(self.tello.get_battery())
                    print(text)
                    cv2.putText(debug_frame, text, (50, 50 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Drone View', debug_frame)
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

