import sys
if __name__ == "__main__":
    user_input = sys.argv[1]
    hex_output = ''.join(f"{ord(char):02X}" for char in user_input)
    hex_output = hex_output.replace('E', '*').replace('F', '#')
print(hex_output)

