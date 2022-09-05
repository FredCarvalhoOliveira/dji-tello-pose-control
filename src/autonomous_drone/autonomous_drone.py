from djitellopy import Tello
from src.pose_detection.body import Body
from src.autonomous_drone.non_blocking_wait import NonBlockingWait

class AutonomousDrone:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.set_speed(10)
        self.tello.streamoff()
        self.tello.streamon()

        self.body_estimation = Body('../res/model/body_pose_model.pth')

        self.wait = NonBlockingWait()

    def takeoff(self):
        self.tello.takeoff()
        self.wait.wait_millis(3000)

    def land(self):
        pass

    def calc_speeds(self):
        pass

    def update_motor_speeds(self):
        pass

    def run(self):
        pass

