dtmf=$(python3 bytes_to_dtmf.py "$1")
echo dtmf is $dtmf
python3 DTMFencode.py $dtmf $2 $3

