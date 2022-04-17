from lib.detection_model import load_net, detect
import numpy as np
import cv2
import grpc
from os import path, environ
from concurrent import futures

import logging

from lib.grpc import spaghetticheck_pb2_grpc
from lib.grpc import spaghetticheck_pb2 as sc_pb2

THRESH = 0.08

model_dir = path.join(path.dirname(path.realpath(__file__)), 'model')
net_main, meta_main = load_net(path.join(model_dir, 'model.cfg'), path.join(model_dir, 'model.weights'), path.join(model_dir, 'model.meta'))

def analyze_image(image):
    # Load the modelimg = cv2.imdecode(img_array, -1)
    img_array = np.array(bytearray(image), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    detections = detect(net_main, meta_main, img, thresh=THRESH)
    result = sc_pb2.AnalyzedFrame()

    for x in detections:
        hit = result.Hits.add()
        hit.Confidence = x[1]
        hit.Class = x[0]
        hit.ClassId = x[3]

        p = sc_pb2.Placement()
        y = x[2]
        p.X = y[0]
        p.Y = y[1]
        p.Width = y[2]
        p.Height = y[3]
        hit.Placement.CopyFrom(p)

    return result

class ImageAnalyzer(spaghetticheck_pb2_grpc.ImageAnalyzeServicer):
    def AnalyzeImage(self, request: sc_pb2.Image, context):
        return analyze_image(request.Data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spaghetticheck_pb2_grpc.add_ImageAnalyzeServicer_to_server(ImageAnalyzer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at", '[::]:50051')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()