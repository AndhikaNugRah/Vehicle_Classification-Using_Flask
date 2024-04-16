# Import necessary libraries
import os
import uuid
import flask
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, send_file
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Create a Flask application instance
app = Flask(__name__)

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the pre-trained Keras model (make sure the path is correct)
model = load_model(os.path.join(BASE_DIR, 'model.hdf5'))

# Define allowed image file extensions
ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])

# Function to check if a filename has a valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

# List of class labels corresponding to the model's predictions
classes = ['airplane', 'automobile','ship', 'truck']

# Function to preprocess an image and make predictions using the model
def predict(filename, model):
  """Preprocesses an image, makes predictions using the model, 
  and returns top class labels and probabilities."""
  # Load the image with the target size specified for the model
  img = load_img(filename, target_size = (32, 32))
  # Convert the image to a NumPy array
  img = img_to_array(img)
  # Reshape the array to match the model's expected input format
  img = img.reshape(1, 32,32,3)


  # Convert image data to float32 and normalize pixel values (0-1)
  img = img.astype('float32')
  img = img/255.0

  # Make a prediction using the model
  result = model.predict(img)

  # Create a dictionary to temporarily store predictions
  dict_result = {}
  for i in range(3):
	# Map probabilities to class labels
        dict_result[result[0][i]] = classes[i]

  # Sort the predicted probabilities in descending order
  res = result[0]
  res.sort()
  res = res[::-1]

  # Extract the top 3 probabilities
  prob = res[:3]

  # Initialize empty lists for class labels and probabilities
  class_result = []
  prob_result = []

  # Loop through the top 3 probabilities
  for i in range(3):
# Check if probability corresponds to a class
      if prob[i] in dict_result:
 # Append class label
          class_result.append(dict_result[prob[i]])
 # Calculate and append probability as percentage
          prob_result.append((prob[i]*100).round(2))

  # Return the top class labels and probabilities
  return class_result, prob_result

# Route for the home page (renders index.html)
@app.route('/')
def home():
    return render_template("index.html")

# Route to handle image uploads and predictions (GET/POST)
@app.route('/success', methods=['GET', 'POST'])
def success():
# Initialize error message
    error = ''
# Target directory for uploaded images
    target_img = os.path.join(os.getcwd(), 'static/images')

# Check if form data is submitted (image URL)
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try:
		# Attempt to download the image from the provided URL
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img, filename)

	        # Save the downloaded image
                output = open(img_path, "wb")
                output.write(resource.read())
                output.close()

		# Use the filename for prediction
                img = filename


	        # Make prediction using the downloaded image
                class_result, prob_result = predict(img_path, model)

		# Create a dictionary to store predictions for the template (only top class is shown)
                predictions = {
                    "class1": class_result[0],
                    "prob1": prob_result[0]
                }

	# Handle exceptions during image download, prediction, etc.
            except Exception as e:
		 # Print exception details for debugging (usually in development)
                print(str(e))
		# Generic error message
                error = 'This image from this site is not accesible or inappropriate input'

	# Render success template if there are no errors
            if(len(error) == 0):
                return render_template('success.html', img=img, predictions=predictions)
	 # Render index with error message
            else:
                return render_template('index.html', error=error)

	# Handle uploaded files (continued)
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename
		
		# Make prediction using the uploaded image
                class_result, prob_result = predict(img_path, model)

		# Create a dictionary to store predictions for the template (only top class is shown)
                predictions = {
                    "class1": class_result[0],
                    "prob1": prob_result[0]}

            else:
                error = "Please upload images of jpg, jpeg and png extension only"

	# Render success/index template based on errors and request type (GET/POST)
            if(len(error) == 0):
                return render_template('success.html', img=img, predictions=predictions)
            else:
                return render_template('index.html', error=error)

	# Render index template for initial page load (GET request)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)