from __future__ import absolute_import, division, print_function

import plate_recognition as pr
import alpr_video as ap

from collections import OrderedDict
from PIL import Image

import json
import time
import requests
import tempfile
import cv2

import numpy as np

MYKEY_1 = '318187864ff963c7c74c3c54898cf4413502f51c'
MYKEY_2 = 'a9aa76c228950d8f9704cf8141a4111a6680fee3'

def recognize_img(image_file):
    result = []
    with open(image_file, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp),
            headers={'Authorization': 'Token ' + MYKEY_2})
        result.append(response.json(object_pairs_hook=OrderedDict))
    time.sleep(1)
    #print(json.dumps(result, indent=2))
    return result


def recognize_vid(video_file, start=0, end=400, skip = 3):
    images = []
    result = []
    cap = cv2.VideoCapture(video_file)
    frame_id = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        frame_id += 1
        if skip and frame_id % skip != 0:
            continue
        if start and frame_id < start:
            continue
        if end and frame_id > end:
            break
        print('Reading frame %s' % frame_id)
        fp = tempfile.NamedTemporaryFile()
        im = Image.fromarray(frame)
        images.append(frame)
        im.save(fp, 'JPEG')
        fp.seek(0)
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp),
            headers={'Authorization': 'Token ' + MYKEY_2})
        result.append(response.json())
        time.sleep(1)
    #print(json.dumps(result, indent=2))
    cap.release()
    cv2.destroyAllWindows()
    return images, result