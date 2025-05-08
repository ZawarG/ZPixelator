import os
import shutil
import tempfile
from flask import Flask, render_template, request
import converter
from werkzeug.utils import secure_filename
final_img = ''
app = Flask(__name__)

# uploads for images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/', methods=['GET', 'POST'])
def home():
    # conversion
    converter.clear_prev_images()
    if request.method == 'POST':
        # retrieve amount of pixels inputted
        pixel_amnt = request.form.get('pixel-amnt')
        # retrieve image inputted
        file = request.files.get('image')

        try:
            # find file suffix
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)

            # if neccessary, normalize jpeg to jpg
            if ext.lower() == '.jpeg':
                ext = '.jpg'

            """ # get image path
            initial_img = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            img_path = initial_img.name
            initial_img.close()
            """
            # save image to retrieved path
            try:
                img_path = os.path.join('static','photos',filename)
                file.save(img_path)
                
                print('SAVED-----------------------------------------------------------------------')
            except Exception as e:
                print("ERROR saving file:", str(e))
                return f"Error saving uploaded image: {e}", 500

            # pixelate initial image using converter, retrieving a url
            output_filename = 'pixelated_' + filename
            print(filename)
            converter.imgtopxl(img_path, int(pixel_amnt), output_filename)
            return render_template('home.html', original_url = '/static/photos/' + filename ,img_url = '/static/photos/' + output_filename)

        except Exception as e:
            return f"Error processing image: {str(e)}", 500
    
    # no conversion (default
    return render_template('home.html', original_url = None, img_url=None)

if __name__ == '__main__':
    app.run(debug=False)
