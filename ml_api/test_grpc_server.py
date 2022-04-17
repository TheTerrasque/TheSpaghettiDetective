import argparse
import grpc
from lib.grpc.spaghetticheck_pb2 import Image
from lib.grpc.spaghetticheck_pb2_grpc import ImageAnalyzeStub

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grpc-server", default="localhost:50051")
    parser.add_argument("image", help="Image to test w ith")
    return parser.parse_args()

args =  parse_args()

CHANNEL = grpc.insecure_channel(args.grpc_server)
vc = ImageAnalyzeStub(CHANNEL)

img = open(args.image, "rb").read()
result = vc.AnalyzeImage(Image(Data=img))
print (result)