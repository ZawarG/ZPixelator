import os
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
    # conversion
    if request.method == 'POST':
        # retrieve amount of pixels inputted
        pixel_amnt = request.form.get('pixel-amnt')
        # retrieve image inputted
        file = request.files.get('image')

        try:
            # find file suffix
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)

            # get image path
            initial_img = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            img_path = initial_img.name
            initial_img.close()

            # save image to retrieved path
            file.save(img_path)

            # pixelate initial image using converter, retrieving a url
            final_img = converter.imgtopxl(img_path, int(pixel_amnt), filename)

            # delete temp file
            os.remove(tmp_path)

            return render_template('home.html', img_url = final_img)

        except Exception as e:
            return f"Error processing image: {str(e)}", 500
    
    # no conversion (default)
    return render_template('home.html', img_url=None)

if __name__ == '__main__':
    app.run(debug=False)
