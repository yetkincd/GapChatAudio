import sys
import numpy as np
from scipy.io.wavfile import read, write

def add_noise(input_file, output_file, noise_level_db=0.0):
    """
    Add noise to a WAV file and save the result.

    Parameters:
    - input_file: str, path to the input WAV file.
    - output_file: str, path to save the output WAV file.
    - noise_level_db: float, noise level in decibels (default 0.0 dB).
    """
    # Read the input WAV file
    sample_rate, data = read(input_file)

    # If stereo, use the first channel
    if data.ndim > 1:
        data = data[:, 0]

    # Calculate the RMS (Root Mean Square) of the signal
    signal_rms = np.sqrt(np.mean(np.abs(np.square(data))))
    print("signal_rms: ",signal_rms)

    # Handle the case of silent audio (RMS is 0)
    if signal_rms == 0:
        print("Input audio is silent. No noise added.")
        noisy_data = data  # No noise to add, return the original data
    else:
        # Convert dB to linear scale for the noise level
        noise_level = 10**(noise_level_db / 20)

        # Generate noise with the same RMS as the specified noise level
        noise = np.random.normal(0, signal_rms * noise_level, data.shape)

        # Add noise to the audio signal
        noisy_data = data + noise

    # Clip to ensure values are within the range for int16
    noisy_data = np.clip(noisy_data, -32768, 32767).astype(np.int16)

    # Save the noisy audio to the output file
    write(output_file, sample_rate, noisy_data)
    print(f"Noise added and saved to {output_file}")

def print_usage():
    print(f"Usage: {sys.argv[0]} input_file output_file [noise_level_db]")
    print(f"Example: {sys.argv[0]} input.wav output.wav 5")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print_usage()
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        noise_level_db = float(sys.argv[3]) if len(sys.argv) == 4 else 0.0
        add_noise(input_file, output_file, noise_level_db)
