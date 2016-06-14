#!/bin/sh
cd testing
if [ $? -eq 0 ]; then
    py.test .
    cd ..
fi
