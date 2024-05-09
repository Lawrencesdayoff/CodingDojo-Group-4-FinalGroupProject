# import os
# from werkzeug.utils import secure_filename
from flask import Flask

# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "shhhhhh"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER