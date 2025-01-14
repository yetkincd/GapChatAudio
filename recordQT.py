import sys
import threading
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtCore import Qt, QTimer
import sounddevice as sd
import numpy as np
import wave
import simpleaudio as sa


class AudioRecorder(QDialog):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.init_ui()

        # Audio recording variables
        self.fs = 44100  # Sampling frequency
        self.recording = False
        self.audio_data = []  # To store recorded audio
        self.stream = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.stop_recording)  # Stop recording after 30 seconds

        # Slider and playback variables
        self.playback_obj = None
        self.playing = False
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self.update_slider_position)

    def init_ui(self):
        self.setWindowTitle("Audio Recorder")
        self.setGeometry(100, 100, 480, 150)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(30000)  # 30 seconds in milliseconds
        self.slider.setValue(0)
        self.slider.sliderMoved.connect(self.slider_moved)

        # Buttons
        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        self.save_button = QPushButton("Save")
        self.play_button = QPushButton("Play")
        self.close_button = QPushButton("Close")

        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.save_button.clicked.connect(self.save_audio)
        self.play_button.clicked.connect(self.play_audio)
        self.close_button.clicked.connect(self.close)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_data = []  # Clear previous recordings
            self.slider.setValue(0)
            self.timer.start(30000)  # Set 30-second timer
            self.stream = sd.InputStream(
                samplerate=self.fs,
                channels=1,
                callback=self.audio_callback
            )
            # Start the recording in a separate thread
            self.recording_thread = threading.Thread(target=self.start_stream)
            self.recording_thread.start()

            self.update_slider_during_recording()
            print("Recording started...")

    def start_stream(self):
        self.stream.start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.timer.stop()
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            print("Recording stopped.")

        if self.playing:
            self.stop_playback()

    def save_audio(self):
        if self.audio_data:
            # Combine all recorded audio chunks
            audio_array = np.concatenate(self.audio_data, axis=0)
            # Scale from [-1.0, 1.0] to 16-bit integer range [-32768, 32767]
            audio_array = (audio_array * 32767).astype(np.int16)
            # Save to a WAV file
            with wave.open("dtmf.wav", "w") as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16 bits per sample
                wf.setframerate(self.fs)
                wf.writeframes(audio_array.tobytes())
            print("Audio saved as dtmf.wav")
        else:
            print("No audio to save.")

    def play_audio(self):
        if not self.playing and self.audio_data:
            # Combine all recorded audio chunks
            audio_array = np.concatenate(self.audio_data, axis=0)
            # Start playback
            self.audio_wave = (audio_array * 32767).astype(np.int16)  # Convert to 16-bit PCM
            self.playback_obj = sa.play_buffer(self.audio_wave, 1, 2, self.fs)
            self.playing = True
            self.slider.setValue(0)
            self.playback_timer.start(10)  # Update every 10 ms
            print("Playing audio...")

    def stop_playback(self):
        if self.playback_obj and self.playing:
            self.playback_obj.stop()
            self.playing = False
            self.playback_timer.stop()
            print("Playback stopped.")

    def update_slider_during_recording(self):
        if self.recording:
            current_position = self.slider.value()
            if current_position < 30000:
                self.slider.setValue(current_position + 10)
                QTimer.singleShot(10, self.update_slider_during_recording)

    def update_slider_position(self):
        if self.playback_obj and self.playing:
            position = self.slider.value()
            if position < 30000:
                self.slider.setValue(position + 10)
            else:
                self.stop_playback()

    def slider_moved(self, value):
        if self.playing:
            # Adjust playback position when slider is moved
            new_position = int(value / 1000 * self.fs)  # Convert slider value to samples
            if self.playback_obj:
                self.stop_playback()
                start_sample = new_position
                audio_array = np.concatenate(self.audio_data, axis=0)
                self.audio_wave = (audio_array[start_sample:] * 32767).astype(np.int16)
                self.playback_obj = sa.play_buffer(self.audio_wave, 1, 2, self.fs)
                self.playing = True
                self.playback_timer.start(10)

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data.append(indata.copy())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = AudioRecorder()
    dialog.show()
    sys.exit(app.exec_())
