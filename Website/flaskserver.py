from flask import Flask, redirect, render_template, request, jsonify, url_for
from PIL import Image
import numpy as np
import os
import re

app = Flask(__name__)

def text_to_binary(text):
    text += "911"
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    print(binary_message)
    return binary_message

def conceal_message(image_file, binary_message):
    image = Image.open(image_file, 'r')
    image_array = np.array(list(image.getdata()))
    width, height = image.size
    
    # print(image_array)
    
    if image.mode == "RGBA":
        channels = 4

    else:
        channels = 3

    pixels = image_array.size // channels

    bit_counter = 0
    
    for i in range(pixels):
        for j in range(channels):
            if bit_counter < len(binary_message):
                image_array[i][j] = int(bin(image_array[i][j])[2:-1] + binary_message[bit_counter],2)
                bit_counter += 1
            else:
                break
                
    image_array = image_array.reshape(height, width, channels)
    concealed_image = Image.fromarray(image_array.astype('uint8'), image.mode)
    
    

    save_dir = 'Website/Favorite'
    os.makedirs(save_dir, exist_ok=True)

    # Save the processed image
    image_path = str(image_file)
    pattern = r"'([^\/]+)\."
    match = re.search(pattern, image_path)
    filename = match.group(1)
    concealed_image_path = os.path.join(save_dir, '{}.png'.format(filename))
    # print(np.array(list(concealed_image.getdata())))
    concealed_image.save(concealed_image_path)
    
    return concealed_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    # Receive image and message data from the frontend
    image_file = request.files['image']
    message = request.form['message']

    # Convert the message to binary format
    binary_message = text_to_binary(message)

    # Process the image and conceal the message
    concealed_image_path = conceal_message(image_file, binary_message)

    # Send the path to the processed image back to the frontend
    return jsonify({'image_path': concealed_image_path})

if __name__ == '__main__':
    app.run(debug=True)
