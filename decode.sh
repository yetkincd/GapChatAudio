dtmf="$(python3 DTMFdecode.py $1)"
echo dtmf detected
echo dtmf string is $dtmf
python3 dtmf_to_bytes.py $dtmf
