import numpy as np
import PIL.Image
import sys

def extract_lsb(fname):
    image = PIL.Image.open(fname, 'r')

    image_arr = np.array(list(image.getdata()))

    channels = 4 if image.mode == "RGBA" else 3

    pixels = image_arr.size // channels # Computer pixel value
    
    messages_bits = ""
    for i in range(pixels):
        for j in range(0,3):
            last_bit = bin(image_arr[i][j])[2:] # Omit the "0b"
            messages_bits += last_bit[-1] # Add the last character of the last_bit string to messages_bits
    print(messages_bits[0:7])
    return messages_bits
   
    
def main():
    # Check for valid argument
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <Processed Image>")
        sys.exit(1)
    
    processed_img = sys.argv[1]
    
    bits = extract_lsb(processed_img)
    
    messages_list = [bits[i:i+8] for i in range(0, len(bits), 8)] # Split every 8 characters into different list index
    string_message = ""
    for k in range(len(messages_list)):
        dec = int(messages_list[k], 2) # convert binary to a decimal value
        string_message += chr(dec) # convert decimal value to ASCII value and add it to the string_message
        
        # Detect if the character is "1", and its previous character is "1"
        # If yes, break the for-loop
        if (messages_list[k] == "00110001" and messages_list[k-1] == "00110001"): 
            break
        
    print(string_message)
    
    
if __name__ == "__main__":
    main()