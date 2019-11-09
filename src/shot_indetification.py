import cv2 as cv
import numpy as np


def identify_shot(path_to_video):
    model = cv.dnn.readNetFromCaffe('../caffe_model/deploy.prototxt.txt',
                                    '../caffe_model/res10_300x300_ssd_iter_140000.caffemodel')
    vid = cv.VideoCapture(path_to_video)

    (W, H) = None, None
    percentages = []
    while True:
        (grabbed, frame) = vid.read()
        if not grabbed:
            break

        if W is None or H is None:
            (H, W) = frame.shape[:2]

        blob = cv.dnn.blobFromImage(frame, 1, (300, 300), (104.0, 177.0, 123.0))
        model.setInput(blob)
        detections = model.forward()

        largest_face = 0
        for i in range(0, detections.shape[2]):
            if detections[0, 0, i, 2] > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                area_of_face = (box[3] - box[1]) * (box[2] - box[0])

                if area_of_face > largest_face:
                    largest_face = area_of_face

        if largest_face > 0:
            percentages.append(largest_face / (W * H))

    return np.mean(percentages)


print(identify_shot('../test_data/taxi_driver_004-0.mov'))
