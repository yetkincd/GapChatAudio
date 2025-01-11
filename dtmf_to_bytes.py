import sys

if __name__ == "__main__":
    # Handle UTF-8 input/output
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Check for arguments
    if len(sys.argv) < 2:
        print("Usage: python decode.py <modified_hex>")
        sys.exit(1)

    # Get modified hex input
    modified_hex = sys.argv[1]
    #print(f"Argument is: {modified_hex}")

    # Replace placeholders back to original hex values
    hex_string = modified_hex.replace('*', 'E').replace('#', 'F')

    try:
        # Decode hex string to bytes and then to UTF-8 string
        original_string = bytes.fromhex(hex_string).decode('utf-8')
        print(original_string)
    except ValueError as e:
        print(f"Error decoding hex string: {e}")

