from djitellopy import Tello
from src.pose_detection.body import Body

class AutonomousDrone:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.set_speed(10)
        self.tello.streamoff()
        self.tello.streamon()

        self.body_estimation = Body('../res/model/body_pose_model.pth')

    def takeoff(self):
        pass

    def land(self):
        pass

    def calc_speeds(self):
        pass

    def update_motor_speeds(self):
        pass

    def run(self):
        pass

