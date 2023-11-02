import os
import gradio as gr
from flask import Flask, request, send_file, abort
from waitress import serve
from werkzeug.utils import secure_filename
from img2img.file_handler import FileHandler
from img2img.utils.generate_file_name import generate_name_file
from img2img.hf_img2img_model import Hfimg2img
from img2img.utils.hex_to_color import hex_to_name
from img2img.create_template import organise_image

file_handler = FileHandler()
new_image = Hfimg2img()

app = Flask(__name__)


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
   

def img2img_gradio(file, hex_color, prompt):
    if file and file_handler.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        random_filename = generate_name_file(filename)
        file.save(os.path.join('received_img', random_filename))
        file_path = "received_img/" + random_filename

        hex_color = hex_to_name(hex_color=hex_color)

        if prompt:
            generated_img_path = new_image.img2img_generate(file_path, prompt, hex_color)
            return generated_img_path
        else:
            abort(400, description="No prompt provided")


image_input = gr.Image(label="Upload an image")
color_input = gr.Textbox(label="Enter a hex color (default: #FFFFFF)", placeholder="#FFFFFF")
prompt_input = gr.Textbox(label="Enter a prompt (default: a beautiful photo)", placeholder="a beautiful photo")

image_output = gr.Image(label="Generated image")
iface_img2img = gr.Interface(fn=img2img_gradio, inputs=[image_input, color_input, prompt_input], outputs=image_output)



@app.route("/gradio_img2img")
def gradio_img2img():
    return iface_img2img.launch(share=True)

# @app.route("/gradio_template_img")
# def gradio_template_img():
#    return iface_template_img.launch()


if __name__ == "__main__":
    app.run()
    # serve(app, host='0.0.0.0', port=8080)
