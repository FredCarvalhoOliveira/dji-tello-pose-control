import cv2
from src.utils.utils import resize


class VisualDebugger:

    @staticmethod
    def draw_keypoints(frame, keypoints, radius=5, color=(255, 0, 0)):
        for pt in keypoints:
            if pt is not None:
                point_coords = (int(pt[0] * frame.shape[1]), int(pt[1] * frame.shape[0]))
                frame = cv2.circle(frame, point_coords, radius, color, -1)
        return frame

    @staticmethod
    def draw_offsets(frame, ref_point, points, thickness=2, color=(255, 255, 0), sec_color=(0, 255, 0)):
        for pt in points:
            if ref_point is not None and pt is not None:
                ref_pt_coords = (int(ref_point[0] * frame.shape[1]), int(ref_point[1] * frame.shape[0]))
                pt_coords = (int(pt[0] * frame.shape[1]), int(pt[1] * frame.shape[0]))
                frame = cv2.rectangle(frame, ref_pt_coords, pt_coords, sec_color, thickness)
                frame = cv2.line(frame, ref_pt_coords, pt_coords, color, thickness)

                offset = (pt_coords[0] - ref_pt_coords[0])/2
                # TODO MAKE THIS BETTER
                offset_str = str(round(pt[0] - ref_point[0], 3))
                frame = cv2.putText(frame,
                                    str(round(pt[0] - ref_point[0], 3)),
                                    (int(ref_pt_coords[0] + offset) - len(offset_str), pt_coords[1] + 15),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    sec_color,
                                    1,
                                    cv2.LINE_AA)
        return frame

