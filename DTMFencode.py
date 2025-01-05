import sys

import numpy as np
from scipy.io.wavfile import write

# Define DTMF frequencies
dtmf_freqs = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}

# Generate DTMF tone
def generate_dtmf_tone(digits, duration=0.4, sample_rate=44100):
    """
    Generate DTMF tones for a given string of digits.

    Parameters:
    - digits: str, string of digits (0-9, *, #).
    - duration: float, duration of each tone in seconds.
    - sample_rate: int, sampling rate in Hz.

    Returns:
    - np.ndarray: The combined DTMF signal as a numpy array.
    """
    signal = np.array([])
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    for digit in digits:
        if digit not in dtmf_freqs:
            continue  # Skip invalid characters
        f1, f2 = dtmf_freqs[digit]
        tone = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
        signal = np.concatenate((signal, tone))
        silence = np.zeros(int(sample_rate * duration))  # Add short silence between tones
        signal = np.concatenate((signal, silence))

    return np.int16(signal / np.max(np.abs(signal)) * 32767)  # Normalize to 16-bit PCM

# Save DTMF tones to a WAV file
def save_to_wav(filename, digits):
    """
    Generate and save DTMF tones to a WAV file.

    Parameters:
    - filename: str, name of the WAV file to save.
    - digits: str, string of digits to convert to DTMF tones.
    """
    sample_rate = 44100
    dtmf_signal = generate_dtmf_tone(digits, sample_rate=sample_rate)
    write(filename, sample_rate, dtmf_signal)  # Save as WAV
    print(f"DTMF tones saved to {filename}")


def print_usage():
    print(sys.argv[0],"DIGITS filename")
    print("example: ",sys.argv[0],"123 123.wav")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
    else:
        digits = sys.argv[1]
        filename = sys.argv[2]
        save_to_wav(filename, digits)
