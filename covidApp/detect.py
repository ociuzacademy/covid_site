from skimage.transform import resize
from skimage.io import imread
import tensorflow as tf
import matplotlib.pyplot as plt


def predict_covid_status(image_path, model_path):

    model = tf.keras.models.load_model(model_path)

    img = imread(image_path)
    img = resize(img, (150, 150, 1))

    img = img.reshape(1, 150, 150, 1)

    predictions = model.predict(img)

    predicted_category_index = predictions.argmax()

    categories = ['Covid patient', 'No Covid Symptoms']

    predicted_category = categories[predicted_category_index]

    return predicted_category