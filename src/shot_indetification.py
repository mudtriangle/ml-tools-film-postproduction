import cv2 as cv
import numpy as np


def identify_shot(path_to_video):
    model = cv.dnn.readNetFromCaffe('../caffe_model/deploy.prototxt.txt',
                                    '../caffe_model/res10_300x300_ssd_iter_140000.caffemodel')
    vid = cv.VideoCapture(path_to_video)

    (W, H) = None, None
    data = {'percentage_area': [],
            'percentage_height': [],
            'percentage_width': [],
            'center_x': [],
            'center_y': []}

    i = 0
    c = 0
    while True:
        i += 1
        (grabbed, frame) = vid.read()
        if not grabbed:
            break

        if W is None or H is None:
            (H, W) = frame.shape[:2]

        if i < 1000:
            continue

        i = 0

        blob = cv.dnn.blobFromImage(frame, 1, (300, 300), (104.0, 177.0, 123.0))
        model.setInput(blob)
        detections = model.forward()

        largest_face = 0
        largest_box = None
        for i in range(0, detections.shape[2]):
            if detections[0, 0, i, 2] > 0.4:
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                box = box.astype(int)

                cv.rectangle(frame, (box[0], box[2]), (box[1], box[3]), (0, 255, 0), 2)

                area_of_face = (box[3] - box[1]) * (box[2] - box[0])

                if area_of_face > largest_face:
                    largest_face = area_of_face
                    largest_box = box

        if largest_face > 0:
            data['percentage_area'].append(largest_face / (W * H))
            data['percentage_height'].append((largest_box[2] - largest_box[0]) / W)
            data['percentage_width'].append((largest_box[3] - largest_box[1]) / H)
            data['center_x'].append((largest_box[3] + largest_box[1]) / (2 * H))
            data['center_y'].append((largest_box[2] + largest_box[0]) / (2 * W))

            print(largest_box)
            print(largest_face / (W * H))
            print((largest_box[2] - largest_box[0]) / W)
            print((largest_box[3] - largest_box[1]) / H)
            print((largest_box[3] + largest_box[1]) / (2 * H))
            print((largest_box[2] + largest_box[0]) / (2 * W))
            print('*********************')

        cv.imwrite('../test_data/test' + str(c) + '.png', frame)
        c += 1

    return data


if __name__ == "__main__":
    shots = identify_shot('../test_data/full_taxi_driver.mp4')
    with open('../test_data/shots.csv', 'w') as f:
        for i in range(len(shots['percentage_area'])):
            f.write('%.5f,%.5f,%.5f,%.5f,%.5f\n' % (shots['percentage_area'][i], shots['percentage_height'][i],
                                                    shots['percentage_width'][i], shots['center_x'][i],
                                                    shots['center_y'][i]))
