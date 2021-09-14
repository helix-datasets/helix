#!/bin/bash

helix build blueprint cmake-cpp example \
    -c minimal-example \
       configuration-example:second_word=example \
    -t replace-example:old=hello,new=goodbye \
       strip
