import json
import os

import cv2
import numpy as np
from loguru import logger
from loko_client.business.fs_client import FSClient
from loko_extensions.business.decorators import extract_value_args
from loko_extensions.model.components import Component, Input, Arg, save_extensions, Dynamic
from sanic import Sanic, json as sjson
from sanic_cors import CORS
import yolov7

from doc.doc import object_detection_doc

app = Sanic("object-detection")
app.static("/web", "/frontend/dist")
CORS(app)

try:
    model = yolov7.load('../resources/yolov7.pt', trace=False)
except AttributeError:
    model = yolov7.load('../resources/yolov7.pt', trace=False)


# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

comp = Component("Object Detector",
                 inputs=[Input(id="image")],
                 args=[Arg(name="keep",
                           value='all',
                           description="Objects to be detected. Existing labels are: 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'. Comma separated"),
                       Arg(name="threshold", type='number', value='0'),
                       Arg(name='save', value=False, description='Save images with bounding boxes', type='boolean'),
                       Dynamic(name='file_path', dynamicType='directories', parent='save', condition="{parent}")],
                 icon="RiDoorOpenLine",
                 description=object_detection_doc)

save_extensions([comp])

gw = 'http://gateway:8080/routes/'
fsclient = FSClient(gateway=gw)


@app.post("/")
@extract_value_args(file=True)
def extract(file, args):
    logger.info(f'ARGS: {args}')
    file = file[0]
    image_np = np.frombuffer(file.body, np.uint8)
    img_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    labels = args.get('keep', 'all')
    labels = [l.strip().lower() for l in labels.split(',')] if labels else []
    save = args.get('save', False)
    threshold = json.loads(args.get('threshold', '0'))
    results = model(img_np)

    # parse results
    predictions = results.pred[0]
    boxes = predictions[:, :4]  # x1, y1, x2, y2
    scores = predictions[:, 4]
    categories = predictions[:, 5]
    ret = []
    for category, score, box in zip(categories, scores, boxes):
        box = [round(el) for el in box.tolist()]
        temp = dict(label=results.names[int(category)], score=float(score), bbox=box)
        logger.info(f'RES: {temp}')
        if labels==['all'] or temp['label'] in labels:
            if temp['score']>threshold:
                ret.append(temp)
    if save:
        file_path = args.get('file_path')['path']
        fname = file.name
        ext = '.'+fname.split('.')[1]
        font = cv2.FONT_HERSHEY_PLAIN
        color = (255, 200, 200)

        bbox_img = img_np.copy()
        for obj in ret:
            x, y, w, h = obj['bbox']
            label = obj['label']
            score = obj['score']
            text = f'{label} - {round(score,2)}'
            roi = bbox_img[y:y + h, x:x + w]
            bbox_img[y:y + roi.shape[0], x:x + roi.shape[1]] = roi
            cv2.rectangle(bbox_img, (x, y), (x + w, y + h), (255, 255, 255), 3)
            (text_width, text_height) = cv2.getTextSize(text, font, fontScale=1, thickness=1)[0]
            text_offset_x, text_offset_y = x, y + 10
            box_coords = (
                (text_offset_x, text_offset_y + 10),
                (text_offset_x + text_width + 10, text_offset_y - text_height - 10))
            cv2.rectangle(bbox_img, box_coords[0], box_coords[1], (0, 0, 0), cv2.FILLED)
            cv2.putText(bbox_img, text, (text_offset_x, text_offset_y), font, fontScale=1, color=color, thickness=1)
        img_byte_arr = cv2.imencode(ext, bbox_img)[1].tobytes()
        fsclient.save(os.path.join(file_path, fname), img_byte_arr)

    return sjson(ret)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, single_process=True)