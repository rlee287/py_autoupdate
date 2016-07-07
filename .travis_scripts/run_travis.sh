#!/bin/sh
# Run tests
cd 'test' || exit 1
py.test --cov-report xml .
test_exit=$?
cd ..
# Ensure that package installs properly
python setup.py develop || exit 1
python -c "import pyautoupdate"
install_exit=$?
python setup.py develop --uninstall
if [ $test_exit = 0 ] && [ $install_exit = 0 ]; then
    exit 0
else
    exit 1
fi
