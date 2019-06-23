api_key = "7f757c7d67a0478aa81c49fd01595b2c"

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

from pprint import pprint



app = ClarifaiApp(api_key=api_key)
model = app.public_models.general_model
model.model_version = 'aa7f35c01e0642fda5cf400f543e7c40'


# get the general model

# predict with the model
with open("/Users/aleksandrmalysev/Yandex.Disk.localized/!PHOTO/xx.07.2018 Андрей, Рыбалка/IMG_1154.JPG", "rb") as file:
    image = ClImage(file_obj=file)
    prediction = model.predict([image])

    pprint(prediction)