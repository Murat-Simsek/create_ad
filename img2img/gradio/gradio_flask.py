
# def img2img_gradio(file, hex_color, prompt):
#     if file and file_handler.allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         random_filename = generate_name_file(filename)
#         file.save(os.path.join('received_img', random_filename))
#         file_path = "received_img/" + random_filename

#         hex_color = hex_to_name(hex_color=hex_color)

#         if prompt:
#             generated_img_path = new_image.img2img_generate(file_path, prompt, hex_color)
#             return generated_img_path
#         else:
#             abort(400, description="No prompt provided")


# image_input = gr.Image(label="Upload an image")
# color_input = gr.Textbox(label="Enter a hex color (default: #FFFFFF)", placeholder="#FFFFFF")
# prompt_input = gr.Textbox(label="Enter a prompt (default: a beautiful photo)", placeholder="a beautiful photo")

# image_output = gr.Image(label="Generated image")
# iface_img2img = gr.Interface(fn=img2img_gradio, inputs=[image_input, color_input, prompt_input], outputs=image_output)



# @app.route("/gradio_img2img")
# def gradio_img2img():
#     return iface_img2img.launch(share=True)