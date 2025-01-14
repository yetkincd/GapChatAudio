rm dtmf.wav
python3 get_input.py > otp_input.txt

ENCODED_INPUT=$(./encode.sh "$(cat otp_input.txt)" dtmf.wav 0.1)

echo $ENCODED_INPUT > encoded.txt
