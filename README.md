# Flask server for template creation.

This flask server use runwayml/stable-diffusion-v1-5 model from HF. 
The first route of the flask server receive an image, hex color and a prompt. Output an image.
Responce time is between 10-15 minute, the actual Google cloud server does not have GPU.
To use the server for the first route use: 


```
import request

url = 'http://34.16.156.84:5000/img2img'
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
```

![Alt text](/image/received_image.jpg "Orginal picture")
The server can be used by the client code in Test_client folder.

