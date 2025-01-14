import sys 
from PyQt5 import QtWidgets,QtGui,QtTest,QtCore
import os
def encode():
    os.popen('/usr/bin/bash otp_encode.sh')
def decode():
    os.popen('/usr/bin/bash otp_decode.sh')
def generate():
    os.popen('/usr/bin/bash generate_randoms.sh')
    
app=QtWidgets.QApplication(sys.argv)
win=QtWidgets.QWidget()
win.setWindowTitle("GapChatAudio Arayüzü")

button1=QtWidgets.QPushButton(win)
button2=QtWidgets.QPushButton(win)
button3=QtWidgets.QPushButton(win)

button1.setText("Gizli Mesaj Gir")
button1.setFont(QtGui.QFont('Arial', 20))
button1.setIcon(QtGui.QIcon("images/speaker.svg"))
button2.setText("Gizli Mesaj Çöz")
button2.setFont(QtGui.QFont('Arial', 20))
button2.setIcon(QtGui.QIcon("images/mic.svg"))
button3.setText("Anahtar Yarat")
button3.setFont(QtGui.QFont('Arial', 20))
button3.setIcon(QtGui.QIcon("images/key.svg"))

button1.setIconSize(QtCore.QSize(64, 64))
button2.setIconSize(QtCore.QSize(64, 64))
button3.setIconSize(QtCore.QSize(64, 64))
        
button1.clicked.connect(encode)
button2.clicked.connect(decode)
button3.clicked.connect(generate)
	
button1.setGeometry(80,60, 320, 100) 
button2.setGeometry(80,220, 320, 100) 
button3.setGeometry(80,380, 320, 100) 

win.setGeometry(0, 60, 480, 540)
win.show()

sys.exit(app.exec_()) 
