from flask import Flask, request, redirect, url_for, render_template, flash
import os
from geopy.geocoders import Nominatim
from werkzeug.utils import secure_filename
from image_processing import image_word
import joblib

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Change this to a secret key for secure session management
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Load the pre-trained machine learning model
model = joblib.load('pred3model (4).pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/home.html')
def home1():
    return render_template('home.html')

@app.route('/blueprint_upload.html')
def upload_html():
    return render_template('blueprint_upload.html')

@app.route('/uploads')
def render():
    return render_template('blueprint_specification.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename("blueprint1.jpg")  # Rename the uploaded file to "blueprint1.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded as blueprint1.jpg')
        return render_template('blueprint_specification.html')
    else:
        flash('Invalid file format. Allowed formats are: png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/specification.html')
def specification():
    return render_template('specification.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        area = float(request.form['area'])
        bedrooms = int(request.form['no_of_bedrooms'])
        bathrooms = int(request.form['no_of_bathrooms'])
        floors = int(request.form['no_of_floors'])
        ATM = int(request.form['ATM'])
        school = int(request.form['school'])
        security = int(request.form['security'])
        carparking = int(request.form['carparking'])
        hospital = int(request.form['hospital'])

        location = request.form['location']
        geolocator = Nominatim(user_agent="geocoder")
        location = geolocator.geocode(location)
        if location is not None:
            latitude = location.latitude
            longitude = location.longitude

        feature_vector = [area, bedrooms, bathrooms, floors, ATM, hospital, school, carparking, security, latitude, longitude]

        prediction = model.predict([feature_vector])

        return render_template('result.html', prediction=int(prediction[0]))

@app.route('/predict-by-blueprint', methods=['POST'])
def predict_by_blueprint():
    if request.method == 'POST':
        original_list = image_word()
        print(original_list)
        area_bedrooms = [[int(item) for item in sub_list] for sub_list in original_list]

        area = area_bedrooms[0][0]
        bedrooms = area_bedrooms[1][0]

        bathrooms = int(request.form['no_of_bathrooms'])
        floors = int(request.form['no_of_floors'])
        ATM = int(request.form['ATM'])
        school = int(request.form['school'])
        security = int(request.form['security'])
        carparking = int(request.form['carparking'])
        hospital = int(request.form['hospital'])

        location = request.form['location']
        geolocator = Nominatim(user_agent="geocoder")
        location = geolocator.geocode(location)
        if location is not None:
            latitude = location.latitude
            longitude = location.longitude

        feature_vector = [area, bedrooms, bathrooms, floors, ATM, hospital, school, carparking, security, latitude, longitude]

        prediction = model.predict([feature_vector])

        return render_template('result.html', prediction=int(prediction[0]/100))



if __name__ == '__main__':
    app.run(debug=True)
