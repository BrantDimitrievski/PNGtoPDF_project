from flask import Flask, request, send_file, abort
from PIL import Image
import os

app = Flask(__name__)
def png_to_pdf(png_path, pdf_path):
    with Image.open(png_path) as img:
        img.convert("RGB").save(pdf_path, "PDF", resolution=100.0, quality=95, optimize=True)

@app.route('/convert', methods=['POST'])
def convert_image():
    print("Received a file for conversion")

    file = request.files['file']
    directory = os.path.abspath('temp')
    png_path = os.path.join(directory, 'temp.png')
    pdf_path = os.path.join(directory, 'output.pdf')

    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    file.save(png_path)
    try:
        png_to_pdf(png_path, pdf_path)
    except Exception as e:
        print("Error during conversion:", e)
        abort(500, description="Error during conversion")

    return send_file(pdf_path, as_attachment=True)
#add code to delete both files

if __name__ == '__main__':
    app.run(debug=True)