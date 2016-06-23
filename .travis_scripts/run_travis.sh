#!/bin/sh
cd 'test'
if [ $? -eq 0 ]; then
    py.test --cov-report xml .
    exit_status=$?
    cd ..
fi
exit $exit_status
