from PIL import Image


def process(in_url, out_url1, out_url2):
    img = Image.open(in_url)
    img.save(out_url1)
    img.save(out_url2)
