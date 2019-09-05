from PIL import Image

from object_detection import image_process

def process(in_url, out_url1, out_url2):

    image_process.run_output(in_url, out_url1)
