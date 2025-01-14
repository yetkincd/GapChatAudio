#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import binascii

# Directory where the binary keys are stored
keys_dir = 'keys'

# Function to XOR input bytes with key bytes
def encrypt_bytes(input_bytes, key_bytes):
    if len(input_bytes) > len(key_bytes):
        raise ValueError("Key is too short for the input data.")
    return bytearray(b ^ k for b, k in zip(input_bytes, key_bytes))

# Function to convert encrypted bytes to DTMF-like text
def bytes_to_dtmf(encrypted_bytes):
    hex_output = ''.join(f"{byte:02X}" for byte in encrypted_bytes)
    return hex_output.replace('E', '*').replace('F', '#')

# Function to convert DTMF-like text back to bytes
def dtmf_to_bytes(dtmf_text):
    hex_text = dtmf_text.replace('*', 'E').replace('#', 'F')
    return binascii.unhexlify(hex_text)

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Encrypt: python otp_crypto.py <text_to_encrypt>")
        print("  Decrypt: python otp_crypto.py -d <FILENAME.bin_HHHH>")
        sys.exit(1)

    if sys.argv[1] == "-d":
        # Decryption mode
        if len(sys.argv) < 3:
            print("Error: Missing encrypted message for decryption.")
            sys.exit(1)
        
        # Parse the input
        input_data = sys.argv[2]
        try:
            key_file, dtmf_text = input_data.split('_', 1)
        except ValueError:
            print("Error: Invalid input format. Expected FILENAME.bin_HHHH.")
            sys.exit(1)

        # Read the key file
        key_path = os.path.join(keys_dir, key_file)
        if not os.path.exists(key_path):
            print(f"Error: Key file '{key_file}' not found in '{keys_dir}'.")
            sys.exit(1)

        with open(key_path, 'rb') as f:
            key_bytes = f.read()

        # Convert DTMF text back to bytes
        encrypted_bytes = dtmf_to_bytes(dtmf_text)

        # Decrypt the message
        try:
            decrypted_bytes = encrypt_bytes(encrypted_bytes, key_bytes)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Output the decrypted message
        print(decrypted_bytes.decode('utf-8'))
    else:
        # Encryption mode
        message = sys.argv[1]
        input_bytes = message.encode('utf-8')

        # Check if the keys directory exists and has files
        if not os.path.exists(keys_dir) or not os.listdir(keys_dir):
            print(f"Error: No key files found in '{keys_dir}'")
            sys.exit(1)

        # Select a random binary key file
        key_file = random.choice(os.listdir(keys_dir))
        key_path = os.path.join(keys_dir, key_file)
        
        # Read the binary key
        with open(key_path, 'rb') as f:
            key_bytes = f.read()

        # Encrypt the input bytes using the key
        try:
            encrypted_bytes = encrypt_bytes(input_bytes, key_bytes)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Convert encrypted bytes to DTMF-like text
        dtmf_output = bytes_to_dtmf(encrypted_bytes)

        # Output the result
        print(f"{key_file}_{dtmf_output}")

if __name__ == "__main__":
    main()
