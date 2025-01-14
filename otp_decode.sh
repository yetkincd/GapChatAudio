python3 recordQT.py
./decode.sh dtmf.wav >otp_encrypted_output.txt
python3 otp_crypto_audio.py -d "$(cat otp_encrypted_output.txt)" >otp_output.txt
python3 messagebox1.py "$(cat otp_output.txt)"
