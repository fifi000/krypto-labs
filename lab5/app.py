from io import BytesIO
from typing import BinaryIO

from stegano import lsb
from PIL.Image import Image
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Flask, request, send_file, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.post('/upload')
def upload():
    # form data
    file: FileStorage = request.files['file']
    message: str = request.form['message']

    if not file or not message:
        return 'Failed to hide message'
    
    # clean filename
    filename = secure_filename(file.filename)

    # hide message
    secret_image: Image = lsb.hide(file.stream, message)

    # Convert PIL Image to BinaryIO
    image_io: BinaryIO = BytesIO()
    secret_image.save(image_io, format='PNG')
    image_io.seek(0)

    return send_file(image_io, as_attachment=True, download_name=f'secret_{filename}')


@app.post('/decode')
def decode():
    # form data
    file = request.files['file']    

    if not file:
        return 'Failed to decode message'

    # decode message
    hidden_message = lsb.reveal(file.stream)

    return {'hidden_message': hidden_message}


if __name__ == '__main__':
    app.run(debug=True)
