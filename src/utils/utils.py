import cv2


def normalize_points(points, frame):
    norm_points = [None for i in range(len(points))]
    for idx, point in enumerate(points):
        if point is not None:
            norm_points[idx] = (point[0]/frame.shape[1], point[1]/frame.shape[0])
    return norm_points


def resize(frame, width: int, inter=cv2.INTER_AREA):
    (h, w) = frame.shape[:2]

    r = width / float(w)
    dim = (width, int(h * r))

    resized = cv2.resize(frame, dim, interpolation=inter)
    return resized




