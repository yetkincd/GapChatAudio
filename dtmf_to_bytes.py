import sys

if __name__ == "__main__":
    modified_hex = sys.argv[1]
    hex_string = modified_hex.replace('*', 'E').replace('#', 'F')
    original_string = ''.join(chr(int(hex_string[i:i+2], 16)) for i in range(0, len(hex_string), 2))
    print(original_string)

