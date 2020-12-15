import io
import re
import time

import numpy as np
from picamera import PiCamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

MAX_WIDTH = 1920
MAX_HEIGHT= 1080

DEFAULT_MODEL_PATH = "models/mobilenet_ssd_v2_object_detect/detect.tflite"
DEFAULT_LABEL_PATH = "models/mobilenet_ssd_v2_object_detect/coco_labels.txt"


class Camera(object):

    def __init__(self):
        self.camera = PiCamera(resolution=(MAX_WIDTH, MAX_HEIGHT), framerate=30)

    def start_stream(self):
        stream = io.BytesIO()
        for _ in self.camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            stream.seek(0)
            self.image = Image.open(stream).convert("RGB").resize((300, 300), Image.ANTIALIAS)
            break

class Detector(object): 

    def __init__(self, model_path=DEFAULT_MODEL_PATH, labels_path=DEFAULT_LABEL_PATH):

        self.labels = self.load_labels(labels_path)
        self.interpreter = Interpreter(model_path)
        self.interpreter.allocate_tensors()
    
    def set_input_tensor(self, image): 
        tensor_index = self.interpreter.get_input_details()[0]["index"]
        input_tensor = self.interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def get_output_tensor(self, index):
        output_details = self.interpreter.get_output_details()[index]
        tensor= np.squeeze(self.interpreter.get_tensor(output_details["index"]))
        return tensor

    def detect_objects(self, image, threshold=0.5): 
        self.set_input_tensor(image)
        self.interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(0)
        classes = self.get_output_tensor(1)
        scores = self.get_output_tensor(2)
        count = int(self.get_output_tensor(3))
        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'class': self.labels[classes[i]],
                'score': scores[i]
                        }
                results.append(result)
        print(results)
        return results

    def load_labels(self, path):
        """Loads the labels file. Supports files with or without index numbers."""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
            return labels

def human_detector():
    
    d = Detector()
    c = Camera()

    _, input_height, input_width, _ = d.interpreter.get_input_details()[0]['shape']

    try: 
        stream = io.BytesIO()
        for _ in c.camera.capture_continuous(stream, format='jpeg', use_video_port=True): 
                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize((input_width, input_height), Image.ANTIALIAS)
                results = d.detect_objects(image)
                for result in results:
                    if result["class"] == "person": 
                        c.camera.start_preview()
                        time.sleep(10)
                        c.camera.stop_preview()
                stream.seek(0)
                stream.truncate()
    finally:
        print('end')
    
if __name__ == "__main__": 
    humanDetector()
