import os
from PIL import Image, ImageDraw, ImageFont

# generated_image = 'img2img/tmpnkanigw__generated.png'
# logo = 'img2img/coffee_logo.png'
# text_punchline = "Your text"
# button_text = "Press here"
# theme_color = "lightblue"


def organise_image(generated_image, logo, text_punchline, button_text, theme_color, saved_final_image):
    # Open the base image and the overlay image
    base_img = Image.open(generated_image)
    overlay_img = Image.open(logo)

    # Define the size of an A4 page in pixels at 300 DPI
    a4_size = (2480, 3508)

    # Resize the images to fit within the A4 page size
    base_img.thumbnail((a4_size[0]/2, a4_size[1]//2))
    overlay_img.thumbnail((a4_size[0]/2, a4_size[1]//2))

    size_overlay = 3
    # Resize the overlay image by a factor of 5
    new_size = (overlay_img.width * size_overlay, overlay_img.height * size_overlay)
    overlay_img = overlay_img.resize(new_size)

    size_base = 3
    # Resize the overlay image by a factor of 5
    new_size_base = (base_img.width * size_base, base_img.height * size_base)
    base_img = base_img.resize(new_size_base)

    # Calculate the position to center the images
    position_base = ((a4_size[0] - base_img.width) // 2, (a4_size[1] - base_img.height) // 2)

    # Calculate the position to center the overlay image
    position_overlay = ((a4_size[0] - overlay_img.width) // 2, (a4_size[1] - overlay_img.height) // 8)

    # Create a white background image
    white_background = Image.new('RGBA', a4_size, (255, 255, 255, 255))

    # Paste the overlay image onto the white background
    white_background.paste(overlay_img, position_overlay)

    # Paste the base image onto the white background
    white_background.paste(base_img, position_base)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(white_background)
    # Load a truetype font with a smaller size
    font = ImageFont.truetype('img2img/font_natural.ttf', 50)

    # Define the position and size of the text box
    text_box_position = (a4_size[0]/10, a4_size[1]-900)  # Increase the distance from the top of the image
    text_box_size = (a4_size[0]/1.25, 400)  # Decrease the height of the text box

    # Add a text box to the image
    draw.rounded_rectangle([text_box_position[0], text_box_position[1], text_box_position[0]+text_box_size[0], text_box_position[1]+text_box_size[1]], fill=theme_color, radius=30)

    # Add text inside the text box
    text = text_punchline
    _, _, text_width, text_height = draw.textbbox((0, 0), text, font=font)

    # Calculate the center coordinates of the text box
    text_box_center = (text_box_position[0] + text_box_size[0]/2, text_box_position[1] + text_box_size[1]/2)

    # Adjust the position of the text to center it within the text box
    text_position = (text_box_center[0] - text_width/2, text_box_center[1] - text_height/2)

    draw.text(text_position, text, fill='black', font=font)

    ##############################

    # Initialize ImageDraw
    draw = ImageDraw.Draw(white_background)
    # Load a truetype font with a smaller size
    font = ImageFont.truetype('img2img/font_natural.ttf', 50)

    # Define the position and size of the text box
    text_box_position = (a4_size[0]/4, a4_size[1]-400)  # Increase the distance from the top of the image
    text_box_size = (a4_size[0]/2, 100)  # Decrease the height of the text box

    # Add a text box to the image
    draw.rounded_rectangle([text_box_position[0], text_box_position[1], text_box_position[0]+text_box_size[0], text_box_position[1]+text_box_size[1]], fill=theme_color, radius=30)

    # Add text inside the text box
    text = button_text
    _, _, text_width, text_height = draw.textbbox((0, 0), text, font=font)

    # Calculate the center coordinates of the text box
    text_box_center = (text_box_position[0] + text_box_size[0]/2, text_box_position[1] + text_box_size[1]/2)

    # Adjust the position of the text to center it within the text box
    text_position = (text_box_center[0] - text_width/2, text_box_center[1] - text_height/2)

    draw.text(text_position, text, fill='black', font=font)

    name, _ = os.path.splitext(saved_final_image)
    # Save the final image
    white_background.save(name + '_final_image.png')
    return name + '_final_image.png'
