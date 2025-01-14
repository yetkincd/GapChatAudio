import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtCore import Qt, QTimer
import sounddevice as sd
import numpy as np
import wave


class AudioRecorder(QDialog):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.init_ui()

        # Audio recording variables
        self.fs = 44100  # Sampling frequency
        self.recording = False
        self.audio_data = []  # To store recorded audio
        self.timer = QTimer()
        self.timer.timeout.connect(self.stop_recording)  # Stop recording after 30 seconds

    def init_ui(self):
        self.setWindowTitle("Audio Recorder")
        self.setGeometry(100, 100, 480, 300)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)

        # Buttons
        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        self.save_button = QPushButton("Save")

        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.save_button.clicked.connect(self.save_audio)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_data = []  # Clear previous recordings
            self.timer.start(30000)  # Set 30-second timer
            self.stream = sd.InputStream(
                samplerate=self.fs,
                channels=1,
                callback=self.audio_callback
            )
            self.stream.start()
            print("Recording started...")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.timer.stop()
            if hasattr(self, "stream"):
                self.stream.stop()
                self.stream.close()
            print("Recording stopped.")

    def save_audio(self):
        if self.audio_data:
            # Combine all recorded audio chunks
            audio_array = np.concatenate(self.audio_data, axis=0)
            # Save to a WAV file
            with wave.open("dtmf.wav", "w") as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16 bits per sample
                wf.setframerate(self.fs)
                wf.writeframes(audio_array.tobytes())
            print("Audio saved as dtmf.wav")
        else:
            print("No audio to save.")

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data.append(indata.copy())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AudioRecorder()
    dialog.show()
    sys.exit(app.exec_())

