__author__      = "Kai Heng Gan"

import numpy as np
import scipy.io.wavfile as wav
import sys
import re
import os

# Function to convert text message to binary
def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

# Function to embed the binary message into the audio signal
def conceal_message(audio_data, message):
    audio_length = len(audio_data)
    message_length = len(message)

    # Generate spreading sequence (pseudo-random sequence)
    np.random.seed(42)  # for reproducibility
    spreading_sequence = np.random.randint(0, 2, audio_length).astype(audio_data.dtype)

    # Modulate the message onto the spreading sequence
    bit_counter = 0
    modulated_message = np.zeros_like(audio_data)
    for i in range(audio_length):
        if bit_counter < message_length:
            for j in range(audio_data.shape[1]):  # Handle multiple channels if present
                modulated_message[i][j] = (audio_data[i][j] + spreading_sequence[i]) % 2  # Modulate message onto spreading sequence
                modulated_message[i][j] &= 0b11111110  # Clear the LSB
                modulated_message[i][j] |= int(message[bit_counter])  # Set the LSB to the message bit
                bit_counter += 1
        else:
            break

    # Combine modulated message with original audio
    stego_audio = audio_data + modulated_message

    return stego_audio

def main():
    if(len(sys.argv) < 4):
        print("Usage: python audioEncoder.py <Aduio File> <Text File> <Output Directory>")
        sys.exit(1)
    
    audio_filename = sys.argv[1]
    textfile = sys.argv[2]
    output_dir = sys.argv[3]

    os.makedirs(output_dir, exist_ok=True)

    # Read audio file
    sample_rate, audio_data = wav.read(audio_filename)

    with open(textfile, 'r') as file:
        message = file.read()

    # Convert text message to binary
    binary_message = text_to_binary(message)

    # Embed binary message into audio
    stego_audio = conceal_message(audio_data, binary_message)

    pattern = r"'([^\/]+)\."
    match = re.search(pattern, audio_filename)
    if match != None:
        filename = match.group(1)

    else:
        if audio_filename.endswith('.wav'):
            filename = audio_filename[:-4]

        else:
            filename = audio_filename

    output_path = os.path.join(output_dir, '{}'.format(filename))
    # Save stego audio to file
    wav.write('{}.wav'.format(output_path), sample_rate, stego_audio)

if __name__ == '__main__':
    main()

