__author__      = "Kai Heng Gan"

import numpy as np
import scipy.io.wavfile as wav
import sys

# Function to convert binary to text
def binary_to_text(binary_message):
    message_list = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    # Convert LSBs to characters
    string = ''

    for i in range(len(message_list)):
        dec = int(message_list[i], 2) # convert binary to a decimal value
        string += chr(dec) # convert decimal value to ASCII value and add it to the string_message

        if(message_list[i] == '00110001'):
            break

    return string

# Function to extract binary message from audio
def extract_message(audio_data, orig_audio):
    extracted_message = ''
    audio_length = len(audio_data)

    modulated_message = audio_data - orig_audio

    # Extract message from modulated audio
    for i in range(audio_length):
        for j in range(audio_data.shape[1]):  # Handle multiple channels if present
                # Extract LSB of each sample
                extracted_bit = modulated_message[i][j] & 0b00000001
                extracted_message += str(extracted_bit)
    
    return extracted_message


def main(): 

    if(len(sys.argv) < 3):
        print("Usage: python audioDecoder.py <Stego Aduio> <Original Audio>")
        sys.exit(1)
    
    stego_filename = sys.argv[1]
    orig_filename = sys.argv[2]

    # Read stego audio file
    sample_rate, stego_audio = wav.read(stego_filename)
    sample_rate, orig_audio = wav.read(orig_filename)

    # Extract binary message from stego audio
    extracted_binary_message = extract_message(stego_audio, orig_audio)

    # Convert binary message to text
    decoded_message = binary_to_text(extracted_binary_message)

    print(decoded_message)

if __name__ == '__main__':
     main()