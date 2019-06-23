
# coding: utf-8

# In[60]:


from client_photolab import ClientPhotolab
import os.path

api = ClientPhotolab()

import os
import sys
import datetime
import imageio
import time
import datetime
import random
from scipy.misc import imresize

from tqdm import tqdm

from scipy.misc import imresize

def create_gif(urls, duration=2):
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


# In[52]:


resourses_filename = 'resources.zip'
if not os.path.exists(resourses_filename):
    api.download_file('http://soft.photolab.me/samples/resources.zip', resourses_filename)

content_filename = 'girl.jpg'
if not os.path.exists(content_filename):
    api.download_file('http://soft.photolab.me/samples/girl.jpg', content_filename)


# _____

# In[53]:


def resize(img, max_h, max_w):
    s = img
    h = min(max_h, img.shape[0])
    w = min(max_w, img.shape[1])
    new_image = imresize(s, (h, w, 3))
    s = imageio.core.util.Array(new_image)
    return imageio.core.util.Array(new_image)


# In[55]:


def upload_image(content_filename):
    original_content_url = api.image_upload(content_filename)
    print('content_url: {}'.format(original_content_url))
    return original_content_url

def get_template_numbers():
    template_numbers = []
    with open("numbers_of_templates.txt") as f:
        s = f.readlines()
        template_numbers = list(map(int, ''.join(s).replace(",", "").replace("\n", " ").split()))
    return template_numbers

template_numbers = get_template_numbers()

def filter_image(image_url, template_number, rotate=10):
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

def make_fun_gif(path):
    global template_numbers
    print("Making gif:", path)
    original_content_url = upload_image(path)
    iterations = 10

    result_image_urls = [original_content_url]

    for i in tqdm(range(iterations)):
        print("{}/{}".format(i, iterations))
        template_number=random.choice(template_numbers)
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
        except Exception as e:
            print("Error with filter:", template_number, e)


    result_image_urls = [r for r in result_image_urls if ".jpg" in r or ".png" in r or ".jpeg" in r]
    print("Images in GIF:", len(result_image_urls))
    output_file = create_gif(result_image_urls)
    res = upload_image(output_file)
    return res
