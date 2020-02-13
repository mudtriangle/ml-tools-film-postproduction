import cv2 as cv
import numpy as np
from scipy.spatial import distance
import math
import pickle
import os

SHOTS = ['long', 'american', 'medium', 'medium close-up', 'close-up']

with open('../test_data/centroids.pkl', 'rb') as f:
    centroids = pickle.load(f)


def classify_shot_file(video_path):
    model = cv.dnn.readNetFromCaffe('../caffe_model/deploy.prototxt.txt',
                                    '../caffe_model/res10_300x300_ssd_iter_140000.caffemodel')
    vid_stream = cv.VideoCapture(video_path)

    (W, H) = None, None
    potential_shots = []
    while True:
        (grabbed, frame) = vid_stream.read()

        if not grabbed:
            break

        if W is None or H is None:
            (H, W) = frame.shape[:2]

        blob = cv.dnn.blobFromImage(frame, 1, (300, 300), (104.0, 177.0, 123.0))
        model.setInput(blob)
        detections = model.forward()

        largest_face = 0
        largest_box = None
        for i in range(0, detections.shape[2]):
            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")

            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                if startX < 0 or startX > W:
                    continue

                if startY < 0 or startY > H:
                    continue

                if endX < 0 or endX > W:
                    continue

                if endY < 0 or endY > H:
                    continue

                largest_face = ((endX - startX) * (endY - startY)) / (W * H)
                largest_box = [startX, startY, endX, endY]

        if largest_face > 0:
            data = np.array([largest_face,
                             (largest_box[2] - largest_box[0]) / W,
                             (largest_box[3] - largest_box[1]) / H])

            dists = np.zeros(len(centroids))

            for i in range(len(centroids)):
                dists[i] = abs(distance.euclidean(data, centroids[i]))
            potential_shots.append(np.argmin(dists))

    type_of_shot, count = np.unique(potential_shots, return_counts=True)
    sum_of_shots = 0
    total_shots = 0
    for i in range(len(type_of_shot)):
        if count[i] > sum(count) / 0.2:
            continue

        sum_of_shots += type_of_shot[i] * count[i]
        total_shots += count[i]

    try:
        mean_shot = sum_of_shots / total_shots
    except ZeroDivisionError:
        return 'Not recognized'
    if 0.9 > mean_shot % 1 > 0.1:
        return SHOTS[math.ceil(mean_shot)] + ' or ' + SHOTS[math.floor(mean_shot)]
    else:
        return SHOTS[int(round(mean_shot))]


def classify_shots(path):
    if os.path.isdir(path):
        shots = {}
        video_files = [path + '/' + x for x in os.listdir(path)]
        for file in video_files:
            shots[file] = classify_shot_file(file)

        return shots

    else:
        return classify_shot_file(path)
