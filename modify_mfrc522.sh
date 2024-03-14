#!/bin/bash

# Path to the MFRC522.py file
FILE_PATH="/usr/local/lib/python3.11/site-packages/mfrc522/MFRC522.py"

# Change "i = 2000" to "i = 5"
sed -i 's/i = 2000/i = 5/g' $FILE_PATH

# Add "time.sleep(0.05)" after line 2016
sed -i '216a\            time.sleep(0.05)' $FILE_PATH