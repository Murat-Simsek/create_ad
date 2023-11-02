import requests


def test_upload():
    url = 'http://34.125.6.50/img2img'
    file_path = '../coffee.png'
    hex_color = "#FFCE30"
    prompt_input = "A glass cup of coffee, detailed, 8k"

    with open(file_path, 'rb') as f:
        response = requests.post(url, files={'file': f}, data={'hex_color': hex_color, 'prompt': prompt_input})

    print(response.status_code)
    assert response.status_code == 200
    # assert 'File uploaded successfully' in response.text

    # Save the image received from the server
    with open('received_image.png', 'wb') as f:
        f.write(response.content)


def test_orginizer():
    url = 'http://localhost:5000/template_img'
    file_path1 = '../img2img/tmpnkanigw__generated.png'
    file_path2 = '../img2img/coffee_logo.png'
    theme_color = "#FFCE80"
    punchline_text = "A glass cup of coffee"
    button_text = "Press here"

    with open(file_path1, 'rb') as f1, open(file_path2, 'rb') as f2:
        response = requests.post(url, files={'file1': f1, 'file2': f2}, data={'theme_color': theme_color, 'punchline_text': punchline_text, 'button_text': button_text })

    print(response.status_code)
    assert response.status_code == 200

    with open('final_orginized_received_image.png', 'wb') as f:
        f.write(response.content)


test_upload()
# test_orginizer()
