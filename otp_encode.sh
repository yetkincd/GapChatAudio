rm dtmf.wav
python3 get_input.py > otp_input.txt

python otp_crypto_audio.py "$(cat otp_input.txt)" >otp_encrypted_input.txt
./encode.sh "$(cat otp_encrypted_input.txt)" dtmf.wav 0.1

