import random
import sys
from datetime import datetime

# Seed the random number generator with the current timestamp
random.seed(datetime.now().timestamp())

# Generate 255 random bytes
result = bytearray(random.randint(0, 255) for _ in range(255))

# Write the bytes directly to stdout
sys.stdout.buffer.write(result)
