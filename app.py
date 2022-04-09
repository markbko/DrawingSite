
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import cv2
import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path)

# configuring the allowed extensions
allowed_extensions = ['jpg', 'png', 'pdf', 'jpeg', 'JPG']
def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions

@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      # Saving the file in the required destination
      if check_file_extension(f.filename):
         f.save(secure_filename(f.filename)) # this will secure the file
      else:
         return 'The file extension is not allowed'
      
      img = cv2.imread(f.filename)
      gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      inverted_img = 255 - gray_image
      blured_img = cv2.GaussianBlur(inverted_img, (21,21), 0)
      inverted_bluredImg = 255 - blured_img
      pencil_sketch = cv2.divide(gray_image, inverted_bluredImg, scale=256.0)
      cv2.imwrite(f.filename, pencil_sketch)
      
      cv2.waitKey(0)
      return send_file(f.filename, as_attachment=True)
		
if __name__ == '__main__':
   app.run(debug = True)