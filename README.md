<html><p><a href="https://loko-ai.com/" target="_blank" rel="noopener"> <img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /> </a></p>
<h1>Object Detection</h1><br></html>

The **Object Detection** extension relies on Yolo-v7 to detect objects from images. 

The "Object Detection" dashboard allows you to upload images and visualize the detected results:
<p align="center">
<img src="https://user-images.githubusercontent.com/30443495/223149734-f7f82bd3-6331-4e70-ac80-4313cd35dec8.png" width="80%" />
</p>

You can directly use the **Object Detector** component into you flow. It accepts a single image in input and returns as output all 
the detected objects:
<p align="center">
<img src="https://user-images.githubusercontent.com/30443495/223150699-733046b7-6ea0-4dbd-9bc8-f97fd6884717.png" width="80%" />
</p>

Within the component, you can set which objects you want to detect, using the `keep` argument. 
The available categories are:
```
'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 
'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 
'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 
'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 
'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 
'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 
'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 
'teddy bear', 'hair drier', 'toothbrush'.
``` 

If you leave this argument to `all`, which is its default value, all the available
categories will be detected.

You can set the minimum score `threshold` to detect an object and a folder where to save the images with their relative bounding boxes (you have to tick `save` first):

<p align="center">
<img src="https://user-images.githubusercontent.com/30443495/223131441-ff529698-5aaa-42f1-9a5a-104a2f76e29b.png" width="80%" />
</p>

If you open your previous selected folder, you'll find the saved images:

<p align="center">
<img src="https://user-images.githubusercontent.com/30443495/223136430-40926846-c6ce-4e61-bc84-7dca3ecb7965.jpg" width="80%" />
</p>

## Configuration

In the file *config.json* you can choose where to mount the volume containing the *YOLO* model:

```
{
  "main": {
    "volumes": [
       "/var/opt/loko/yolo/:/plugin/resources"
       ],
    "gui": {
      "name": "Object Detection"
    }
  }
}
```
