import sys
import numpy as np
from scipy.io.wavfile import read
from scipy.signal import find_peaks, butter, filtfilt
import matplotlib.pyplot as plt

# Define DTMF frequencies
dtmf_freqs = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}

# High-pass filter to remove low-frequency noise
def highpass_filter(data, sample_rate, cutoff=650):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(1, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

# Low-pass filter to remove high-frequency noise
def lowpass_filter(data, sample_rate, cutoff=1700):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# Combine high-pass and low-pass filtering
def bandpass_filter(data, sample_rate):
    data = highpass_filter(data, sample_rate, cutoff=650)
    return lowpass_filter(data, sample_rate, cutoff=1700)

# Detect silent regions to segment tones
def detect_silent_regions(data, sample_rate, threshold=0.02, min_silence_duration=0.1):
    """Detect silent regions in the audio based on amplitude."""
    abs_data = np.abs(data)
    silence_threshold = threshold * np.max(abs_data)
    silence_samples = int(min_silence_duration * sample_rate)
    
    silent_regions = []
    is_silent = False
    start_idx = 0
    
    for i, value in enumerate(abs_data):
        if value < silence_threshold:
            if not is_silent:
                is_silent = True
                start_idx = i
        else:
            if is_silent and i - start_idx >= silence_samples:
                silent_regions.append((start_idx, i))
            is_silent = False
    
    if is_silent and len(data) - start_idx >= silence_samples:
        silent_regions.append((start_idx, len(data)))
    
    return silent_regions

def decode_dtmf(filename, visualize=False):
    # Read the audio file
    sample_rate, data = read(filename)
    
    # Use only one channel if stereo
    if data.ndim > 1:
        data = data[:, 0]

    # Apply band-pass filter to isolate DTMF-relevant frequencies
    data = bandpass_filter(data, sample_rate)

    # Detect silent regions
    silent_regions = detect_silent_regions(data, sample_rate)

    # Segment audio into tones using silence gaps
    detected_digits = []
    start_idx = 0
    for silent_start, silent_end in silent_regions:
        tone_segment = data[start_idx:silent_start]
        start_idx = silent_end

        if len(tone_segment) < int(0.05 * sample_rate):  # Ignore short segments
            continue

        # Compute FFT for the tone segment
        fft_data = np.abs(np.fft.rfft(tone_segment))
        freqs = np.fft.rfftfreq(len(tone_segment), d=1/sample_rate)

        # Detect peaks
        peaks, _ = find_peaks(fft_data, height=0.50 * np.max(fft_data))
        detected_freqs = freqs[peaks]

        # Match frequencies to DTMF tones
        for digit, (f1, f2) in dtmf_freqs.items():
            if (np.any(np.isclose(detected_freqs, f1, atol=10)) and
                    np.any(np.isclose(detected_freqs, f2, atol=10))):
                detected_digits.append(digit)
                break

    return detected_digits

def print_usage():
    print(f"Usage: {sys.argv[0]} [-viz] filename")
    print(f"Example: {sys.argv[0]} -viz 123.wav")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
    else:
        visualize = False
        if "-viz" in sys.argv:
            visualize = True
            sys.argv.remove("-viz")

        if len(sys.argv) < 2:
            print_usage()
        else:
            filename = sys.argv[1]
            try:
                decoded_digits = decode_dtmf(filename, visualize)
                #print("Detected DTMF Tones:", "".join(decoded_digits))
                print("".join(decoded_digits))
            except Exception as e:
                print(f"Error decoding file: {e}")

