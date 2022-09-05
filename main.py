from src.autonomous_drone.autonomous_drone import AutonomousDrone
import cv2

drone = AutonomousDrone()
drone.run(debug=True)


# drone.takeoff()
#
# if drone.wait.has_time_passed():
#     while drone.SHOULD_RUN:
#         frame = drone.get_frame()
#         # keypoints = self.predict_pose(img=frame)
#         # speeds = self.calc_speeds(keypoints=keypoints)
#         # self.update_motor_speeds(speeds=speeds)
#
#         cv2.imshow('Drone View', frame)
#         k = cv2.waitKey(1)
#         if k == ord('q'):
#             break
#         elif k == ord('s'):
#             print('>>> Taking off')
#     # Stop the drone
#     print('>>> Turning off drone')
#     drone.tello.end()