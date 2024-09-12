from flask import Flask, request, render_template
from helpers import get_uploaded_image, process_image_for_bg_removal, save_image_to_static
import os

app = Flask(__name__)

# Ensure the 'static/uploads/' directory exists
os.makedirs('static/uploads/', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_bg', methods=['POST'])
def remove_bg():
    image_file = get_uploaded_image(request)
    
    if image_file is None or image_file.filename == '':
        return render_template('index.html', original_image=None, processed_image=None, download_url=None)

    original_image_path = save_image_to_static(image_file, 'original')
    output_image = process_image_for_bg_removal(image_file)
    processed_image_path = save_image_to_static(output_image, 'processed')
    
    # Create a download URL for the processed image
    download_url = processed_image_path

    return render_template('index.html', original_image=original_image_path, processed_image=processed_image_path, download_url=download_url)

if __name__ == '__main__':
    app.run(debug=True)
