dtmf=$(python3 DTMFdecode2.py $1)
echo dtmf detected
echo dtmf string is $dtmf
python3 dtmf_to_bytes.py $dtmf