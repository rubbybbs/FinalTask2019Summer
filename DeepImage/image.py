from PIL import Image


def process(in_url, out_url):
    img = Image.open(in_url)
    img.save(out_url)
