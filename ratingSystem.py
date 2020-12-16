import cv2
from keras.models import Model, load_model
import numpy as np
from glob import glob

def ratingImages(URLs):
    model = load_model('./trained_model.h5')

    img_test_list = glob('./static/images/*.jpg')
    img_test_list.sort()

    imgs_test_resized = []

    for i, img_path in enumerate(img_test_list):
        stream = open(img_path.encode("utf-8") , "rb")
        bytes = bytearray(stream.read())
        numpyArray = np.asarray(bytes, dtype=np.uint8)
        img = cv2.imdecode(numpyArray , cv2.IMREAD_UNCHANGED)
        
        img_resized = cv2.resize(img, (350, 350))
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_resized = img_resized.astype(np.float32) / 255.
        imgs_test_resized.append(img_resized)

    imgs_test_resized = np.array(imgs_test_resized, dtype=np.float32)

    preds = model.predict(imgs_test_resized)

    max_score = 0
    max_score_img_path = ''
    for i, img in enumerate(imgs_test_resized):
        score = float(preds[i])
        if score > max_score:
            max_score = score
            max_score_img_path = URLs[i]
    max_score = round(max_score, 2)

    return max_score, max_score_img_path