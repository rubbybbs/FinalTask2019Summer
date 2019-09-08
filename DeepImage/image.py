from object_detection import image_process
from fast_style_transfer import evaluate


def process(in_url, out_url1, out_url2):
    image_process.run_output(in_url, out_url1)
    evaluate.run(in_url, out_url2)
