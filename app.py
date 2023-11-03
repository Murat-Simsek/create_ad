import os

from flask import Flask, request, send_file, abort
from werkzeug.utils import secure_filename
from img2img.file_handler import FileHandler
from img2img.utils.generate_file_name import generate_name_file
from img2img.hf_img2img_model import Hfimg2img
from img2img.utils.hex_to_color import hex_to_name
from img2img.create_template import organise_image

file_handler = FileHandler()
new_image = Hfimg2img()

app = Flask(__name__)

@app.route("/")
def hello():
   return "Hello World!"

@app.route("/img2img",  methods=['POST'])
def img2img():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file_handler.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        random_filename = generate_name_file(filename)
        file.save(os.path.join('received_img', random_filename))
        file_path = "received_img/" + random_filename

        hex_color = request.form.get('hex_color', '#FFFFFF')  # Default to white if no hex color is provided
        hex_color = hex_to_name(hex_color=hex_color)

        if 'prompt' not in request.form:
            abort(400, description="No prompt provided")
        prompt = request.form.get('prompt', "a beautiful photo")  # Default prompt if empty

        # Hf code, return image.
        generated_img_path = new_image.img2img_generate(file_path, prompt, hex_color)
        return send_file(os.path.join(generated_img_path))


@app.route("/template_img",  methods=['POST'])
def template_img():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'No file part'
    file1 = request.files['file1']
    file2 = request.files['file2']
    if file1.filename == '' or file2.filename == '':
        return 'No selected file'
    if file1 and file_handler.allowed_file(file1.filename) and file2 and file_handler.allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        random_filename1 = generate_name_file(filename1)
        random_filename2 = generate_name_file(filename2)
        file1.save(os.path.join('received_img', random_filename1))
        file2.save(os.path.join('received_img', random_filename2))
        generated_img = "received_img/" + random_filename1
        logo = "received_img/" + random_filename2

        theme_color = request.form.get('theme_color', '#FFFFFF')  # Default to white if no theme color is provided
        theme_color = hex_to_name(hex_color=theme_color)

        punchline_text = request.form.get('punchline_text', "a beautiful photo")  # Default punchline if empty
        button_text = request.form.get('button_text', "Press here")

        # Orginized image code, return image.
        path_to_final_img = organise_image(generated_image= generated_img, logo=logo, theme_color=theme_color, text_punchline=punchline_text, button_text=button_text, saved_final_image=generated_img)

        return send_file(os.path.join(path_to_final_img))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
