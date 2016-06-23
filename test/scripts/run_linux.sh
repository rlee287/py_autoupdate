#!/bin/sh
cd 'test'
if [ $? -eq 0 ]; then
    py.test .
    exit_status=$?
    cd ..
fi
exit exit_status
