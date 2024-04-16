# Overview 
This repository implements a Flask API that enables vehicle classification using a pre-trained convolutional neural network (CNN) model. The model is trained on the CIFAR-10 image dataset, which consists of 60,000 labeled images of various vehicles (airplanes, automobiles, ships, trucks).

# Key Features
1.Pre-trained Model: Leverages a pre-trained model (model.hdf5) for efficient vehicle classification.
2.Flask API: Provides a user-friendly interface for image classification through a web API.
3.Image Upload: Users can upload images for classification through the API.
4.Prediction Results: The API returns the predicted class label (e.g., "airplane") and its probability.

# Prerequisites
Python 3.x (https://www.python.org/downloads/)
Necessary libraries:
Flask 
TensorFlow (https://www.tensorflow.org/)
NumPy (https://numpy.org/)

# Installation
1.Clone this repository to your local machine.
2.Open a terminal or command prompt and navigate to the project directory.
3.Install the required libraries:
4.Running the Application
5.Start a Python interpreter (e.g., using Spyder or your preferred IDE).
6.In the interpreter, navigate to the project directory (where "flask_app.py" is located).
7.Execute the flask_app.py to run the Flask application:
8.The application will typically start on http://127.0.0.1:5000/ (or a similar URL) by default. You can view it in your web browser.

# Using the API
Here's how you can interact with the API to classify an image:
1.Prepare your image: Ensure the image is in a supported format (e.g., JPG, PNG).
2.Upload the image by put the file in column and click "up here" or you can use the put url of the image (not a website of the image)
3.Receive predictions: The API will process the image, make a prediction using the pre-trained model, and return a JSON response containing the predicted class label and its probability.
