import cv2 as cv
import numpy as np
from scipy.spatial import distance
from scipy.stats import mode
import pickle
import json

SHOTS = ['medium close-up', 'medium', 'medium wide', 'wide', 'close-up']

model = cv.dnn.readNetFromCaffe('../caffe_model/deploy.prototxt.txt',
                                '../caffe_model/res10_300x300_ssd_iter_140000.caffemodel')
vid_stream = cv.VideoCapture('../test_liene/video/A011_07091319_C006.mov')

with open('../test_data/centroids.pkl', 'rb') as f:
    centroids = pickle.load(f)

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
        data = np.array([largest_face, (largest_box[2] - largest_box[0]) / W, (largest_box[3] - largest_box[1]) / H])

        dists = np.zeros(len(centroids))

        for i in range(len(centroids)):
            dists[i] = abs(distance.euclidean(data, centroids[i]))
        potential_shots.append(np.argmin(dists))

with open('../test_liene/file_structure.json', 'r') as f:
    file_structure = json.load(f)

m = mode(potential_shots)[0][0]
print(np.unique(potential_shots, return_counts=True))

file_structure['../test_liene/video/A011_07091319_C006.mov'] = {'type_of_shot': SHOTS[m]}

with open('../test_liene/file_structure.json', 'w') as f:
    json.dump(file_structure, f)
