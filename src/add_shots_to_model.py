import cv2 as cv
import numpy as np
import pickle

model = cv.dnn.readNetFromCaffe('../caffe_model/deploy.prototxt.txt',
                                '../caffe_model/res10_300x300_ssd_iter_140000.caffemodel')
vid_stream = cv.VideoCapture('../test_data/the_big_sick.mp4')

(W, H) = None, None

with open('../test_data/shots.pkl', 'rb') as f:
    data = pickle.load(f)

print(len(data['percentage_area']))

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
        data['percentage_area'].append(largest_face)
        data['percentage_width'].append((largest_box[2] - largest_box[0]) / W)
        data['percentage_height'].append((largest_box[3] - largest_box[1]) / H)
        data['center_x'].append((largest_box[3] + largest_box[1]) / (2 * H))
        data['center_y'].append((largest_box[2] + largest_box[0]) / (2 * W))

        print(largest_box)
        print(largest_face)
        print((largest_box[2] - largest_box[0]) / W)
        print((largest_box[3] - largest_box[1]) / H)
        print((largest_box[3] + largest_box[1]) / (2 * H))
        print((largest_box[2] + largest_box[0]) / (2 * W))
        print('*********************')

with open('../test_data/shots.pkl', 'wb') as f:
    pickle.dump(data, f)
