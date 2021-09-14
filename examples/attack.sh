#!/bin/bash

# Combine a collection of ATT&CK components to do something interesting.
# 
# This example uses a number of ATT&CK components to:
#   1. Download a remote file.
#   2. Compress the file.
#   3. Encrypt the compressed file.
#   4. Delete unencrypted and uncompressed files.
#   5. Timestomp the compressed, encrypted download

helix build blueprint cmake-cpp attack \
    -c linux-libcurl-remote-file-copy:url=http://www.google.com/commands.txt,output=commands \
       linux-zlib-compress-data-compressed:input=commands,output=commands.gz \
       linux-openssl-aes-encrypt-data-encrypted:input=commands.gz,output=commands.gz.enc,key=abcdefghijklmnopqrstuvwxyzabcdef \
       linux-remove-file-deletion:path=commands \
       linux-remove-file-deletion:path=commands.gz \
       linux-utime-timestomp:path=commands.gz.enc,timestamp="2010-01-01 12:00:00" \
    -t strip \
    --verbose
