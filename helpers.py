from rembg import remove
from PIL import Image
import io
import os
import uuid

def get_uploaded_image(request):
    if 'image' not in request.files:
        return None
    return request.files['image']

def process_image_for_bg_removal(image_file):
    image_file.seek(0)
    input_image = image_file.read()

    # Check the size of the file to ensure it’s read properly
    if not input_image:
        raise Exception("Uploaded image file is empty or not readable")

    # Try removing the background
    try:
        output_image = remove(input_image)
        return output_image
    except Exception as e:
        raise Exception(f"Error during background removal: {e}")

def save_image_to_static(image_file, image_type):
    """
    Saves the image to the 'static/uploads' directory.
    The image_type can be 'original' or 'processed'.
    Returns the relative path to the image for rendering in the HTML.
    """
    # Generate a unique file name with UUID
    unique_filename = f'{uuid.uuid4().hex}_{image_type}_image.png'
    file_path = os.path.join('static/uploads', unique_filename)

    if image_type == 'original':
        img = Image.open(image_file)
    else:
        img = Image.open(io.BytesIO(image_file))

    # Save the image to the unique file path
    img.save(file_path, 'PNG')
    
    return f'/static/uploads/{unique_filename}'
