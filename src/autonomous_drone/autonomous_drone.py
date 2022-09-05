from djitellopy import Tello
from src.pose_detection.body import Body
from src.autonomous_drone.non_blocking_wait import NonBlockingWait
from typing import List, Tuple
import cv2

class AutonomousDrone:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.set_speed(10)
        self.tello.streamoff()
        self.tello.streamon()

        self.frame_read = self.tello.get_frame_read()

        self.pose_model = Body('../res/model/body_pose_model.pth')

        self.wait = NonBlockingWait()
        self.SHOULD_RUN = True

    def takeoff(self):
        self.tello.takeoff()
        self.wait.wait_millis(3000)

    def land(self):
        pass

    def get_frame(self):
        return self.frame_read.frame

    def predict_pose(self, img) -> List[Tuple]:
        candidate, subset = self.pose_model(img)

    def calc_speeds(self, keypoints: List[Tuple]) -> List[int]:
        pass

    def update_motor_speeds(self, speeds: List[int]):
        pass

    def run(self, debug=False):
        self.takeoff()

        if self.wait.has_time_passed():
            while self.SHOULD_RUN:
                frame = self.get_frame()
                keypoints = self.predict_pose(img=frame)
                speeds = self.calc_speeds(keypoints=keypoints)
                self.update_motor_speeds(speeds=speeds)

                cv2.imshow('Drone View', frame)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break
                elif k == ord('s'):
                    print('>>> Start take off')
            # Stop the drone
            self.tello.end()

    def stop(self):
        self.SHOULD_RUN = False

