import os
import shutil
import tempfile
from flask import Flask, render_template, request
import converter
from werkzeug.utils import secure_filename

app = Flask(__name__)

# uploads for images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home():
    # set default url values
    original_url = None
    img_url = None

    if request.method == 'POST':
        pixel_amnt = request.form.get('pixel-amnt') # retrieve amount of pixels inputted
        file = request.files.get('image') # retrieve image inputted
        original_url = request.form.get("original_url") # retrieve original url (in case it exists)

        # ensure file and filename are not empty (a new image was uploaded)
        if (file) and (file.filename !=''):
            # conversion
            converter.clear_prev_images()

            # find file suffix
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)

            # if neccessary, normalize jpeg to jpg
            if ext.lower() == '.jpeg':
                ext = '.jpg'
            
            # save uploaded image to original_url
            try:
                original_path = os.path.join('static','photos',filename)

                if os.path.exists(original_path):
                    print(f"Image already exists: {original_path}")
                else:
                    file.save(original_path)
                    original_url = os.path.join('static','photos',filename)
                
                print('SAVED-----------------------------------------------------------------------')
            except Exception as e:
                print("ERROR saving file:", e)
                return f"Error saving uploaded image: {e}", 500
            
            # pixelate initial image using converter, retrieving a url
            output_filename = 'pixelated_' + filename
            print(filename)
            converter.imgtopxl(original_path, int(pixel_amnt), output_filename)

            # original_path = os.path.join('static','photos',filename)
            # file.save(original_path)
            # original_url = os.path.join('static','photos',filename)

        # if file and filename are empty, but a previous image exists
        elif (original_url != None):
            # use already saved image
            filename = os.path.basename(original_url)
            original_path = os.path.join(app.root_path, 'static', 'photos', filename)
        
        else:
            return f"Error processing image"
        
        # pixelate initial image using converter, retrieving a url
        output_filename = 'pixelated_' + filename
        converter.imgtopxl(original_path, int(pixel_amnt), output_filename)

        # apply new url
        img_url = '/static/photos/' + output_filename
    
    return render_template('home.html', original_url = original_url, img_url=img_url)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=False)
