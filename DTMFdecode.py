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

def decode_dtmf(filename, visualize=False):
    # Read the audio file
    sample_rate, data = read(filename)
    
    # Use only one channel if stereo
    if data.ndim > 1:
        data = data[:, 0]

    # Apply band-pass filter to isolate DTMF-relevant frequencies
    data = bandpass_filter(data, sample_rate)

    n = len(data)
    winlen = int(0.1 * sample_rate)  # Window length
    winstep = winlen // 2           # Overlap by half window size
    detected_digits = []

    if visualize:
        plt.figure(figsize=(12, 6))

    for idx, i in enumerate(range(0, n - winlen, winstep)):
        # Extract a window of data
        windata = data[i:i + winlen]
        windata = windata - np.mean(windata)  # Remove residual DC offset

        # Compute FFT for the window
        fft_data = np.abs(np.fft.rfft(windata))
        freqs = np.fft.rfftfreq(len(windata), d=1/sample_rate)

        # Detect peaks
        peaks, _ = find_peaks(fft_data, height=0.50 * np.max(fft_data))  # Adjust threshold
        detected_freqs = freqs[peaks]

        # Check for pairs of frequencies corresponding to DTMF tones
        for digit, (f1, f2) in dtmf_freqs.items():
            if (np.any(np.isclose(detected_freqs, f1, atol=10)) and
                    np.any(np.isclose(detected_freqs, f2, atol=10))):
                if not detected_digits or detected_digits[-1] != digit:
                    detected_digits.append(digit)

        # Visualize the current window and its FFT if visualization is enabled
        if visualize:
            plt.subplot(2, 1, 1)
            plt.plot(windata, label=f"Window {idx + 1}")
            plt.xlabel("Samples")
            plt.ylabel("Amplitude")
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(freqs, fft_data, label=f"FFT {idx + 1}")
            plt.scatter(freqs[peaks], fft_data[peaks], color='red', label="Peaks")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Magnitude")
            plt.legend()

            plt.pause(0.5)  # Pause for half a second to visualize each step
            plt.clf()

    if visualize:
        plt.close()

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
                print("Detected DTMF Tones:", "".join(decoded_digits))
            except Exception as e:
                print(f"Error decoding file: {e}")
