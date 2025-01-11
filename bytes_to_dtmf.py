import sys

if __name__ == "__main__":
    # Handle UTF-8 input/output
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Check for arguments
    if len(sys.argv) < 2:
        print("Usage: python encode.py <user_input>")
        sys.exit(1)

    # Get user input
    user_input = sys.argv[1]

    # Encode to UTF-8 and generate hex representation
    hex_output = ''.join(f"{byte:02X}" for byte in user_input.encode('utf-8'))

    # Replace E and F with placeholders
    hex_output = hex_output.replace('E', '*').replace('F', '#')

    print(hex_output)

