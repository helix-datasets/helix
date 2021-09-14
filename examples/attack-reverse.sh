#!/bin/bash

# Inverse of ATT&CK binary - to demonstrate success

helix build blueprint cmake-cpp reverse \
    -c linux-openssl-aes-decrypt-data-encrypted:input=commands.gz.enc,output=commands.gz,key=abcdefghijklmnopqrstuvwxyzabcdef \
       linux-zlib-decompress-data-compressed:input=commands.gz,output=commands \
       linux-remove-file-deletion:path=commands.gz \
    --verbose
