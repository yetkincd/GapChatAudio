import sys
#encrypt_bytes.py input_filename key_filename output_filename


if __name__ == "__main__":
    if len(sys.argv) < 4 :
        print("use "+sys.argv[0]+" input_filename key_filename output_filename")
        exit()
    input_filename = sys.argv[1]
    key_filename = sys.argv[2]
    output_filename = sys.argv[3]
#{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}
    inputTxt = bytearray(open(input_filename, "rb").read())
    keyTxt = bytearray(open(key_filename, "rb").read())

    if len(inputTxt) > len(keyTxt) :
        print("error")
    else:
        outputTxt = bytearray((len(inputTxt)))    
        for i in range(0,len(inputTxt)) :
            outputTxt[i] = inputTxt[i] ^ keyTxt[i]
        with open(output_filename, 'wb') as f:
            f.write(outputTxt)





    encrypting = ''




