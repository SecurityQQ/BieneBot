
# coding: utf-8
import os
import sys
import datetime
import imageio
import time
import datetime
import random
import pandas as pd
from tqdm import tqdm
from scipy.misc import imresize

from client_photolab import ClientPhotolab
api = ClientPhotolab()

GIF_DURATION = 1.5
FILTER_ITERATIONS = 6
DEFAULT_ROTATE = 10

def get_template_numbers():
    template_numbers = []
    with open("numbers_of_templates.txt") as f:
        s = f.readlines()
        template_numbers = list(map(int, ''.join(s).replace(",", "").replace("\n", " ").split()))
    return template_numbers

template_numbers = get_template_numbers()

def create_gif(urls, duration=GIF_DURATION):
    images = []
    for url in urls:
        s = imageio.imread(url)
        if s.shape[0] > 700 and s.shape[1] > 700:
            new_image = imresize(s, (s.shape[0]//2, s.shape[1]//2, 3))
        else:
            new_image = s
        s = imageio.core.util.Image(new_image)
        images.append(s)
    output_file = 'gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    imageio.mimsave(output_file, images, duration=duration)
    return output_file

def download_resources():
    resourses_filename = 'resources.zip'
    if not os.path.exists(resourses_filename):
        api.download_file('http://soft.photolab.me/samples/resources.zip', resourses_filename)

    content_filename = 'girl.jpg'
    if not os.path.exists(content_filename):
        api.download_file('http://soft.photolab.me/samples/girl.jpg', content_filename)


def read_dataset(filepath="./data/asdf - asdf.csv"):
    filepath = "./data/asdf - asdf.csv"
    data = pd.read_csv(filepath, index_col=0)
    data = data[["0", "1", "alex review", "max review"]]

    data = data[
        [data.columns[0], data.columns[1]] + list(data.columns[3:])
    ].fillna(0)
    data = data.rename(columns={
        data.columns[0]: "f", 
        data.columns[1]: "s"
    })
    data["score"] = data[data.columns[2:]].sum(axis=1)
    data = data[["f", "s", "score"]]

    data.score = data.score + 1e-5
    return data

def random_walk(MAX_TEMPLATES=5):
    data = read_dataset()

    next_template = random.choice(data.f.unique())
    template_sequence = [next_template]

    for i in range(MAX_TEMPLATES):
        try:
            data_slice = data[data.f == next_template]
            if data_slice.shape[0] == 0:
                break
            next_template = random.choices(list(data_slice.s), list(data_slice.score))[0]
            template_sequence.append(next_template)
        except Exception as e:
            print(e)
            break
            
    return template_sequence


def resize(img, max_h, max_w):
    s = img
    h = min(max_h, img.shape[0])
    w = min(max_w, img.shape[1])
    new_image = imresize(s, (h, w, 3))
    s = imageio.core.util.Array(new_image)
    return imageio.core.util.Array(new_image)

def upload_image(content_filename):
    original_content_url = api.image_upload(content_filename)
    print('content_url: {}'.format(original_content_url))
    return original_content_url

def filter_image(image_url, template_number, rotate=DEFAULT_ROTATE):
    result_url = api.template_process(
        template_number,
        [{
            'url' : image_url,
            'rotate': rotate,
            'flip' : 0,
            'crop' : '0,0,1,1'
        }]
    )
    return result_url

def make_fun_gif(path, iterations=FILTER_ITERATIONS):
    global template_numbers
    print("Making gif:", path)
    original_content_url = upload_image(path)
    result_image_urls = [original_content_url]
    templates = random_walk(iterations * 5)

    success_i = 0
    print("Templates: ", len(templates))
    for i, template in enumerate(templates):
        print("{}/{}".format(i, iterations))
        template_number=template
        try:
            result_url = filter_image(
                image_url=result_image_urls[-1],
                template_number=template_number,
                rotate=10,
            )

            print('i: {}, result_url: {}'.format(i, result_url))

            # If result is image, not video
            if ".jpg" in result_url or ".png" in result_url or ".jpeg" in result_url:
                result_image_urls.append(result_url)
                success_i = success_i + 1
            else:
                print("Fail: ", i)
            if success_i >= iterations:
                break

        except Exception as e:
            print("Error with filter:", template_number, e)


    result_image_urls = [r for r in result_image_urls if ".jpg" in r or ".png" in r or ".jpeg" in r]
    print("Images in GIF:", len(result_image_urls))
    output_file = create_gif(result_image_urls)
    res = upload_image(output_file)
    return res
