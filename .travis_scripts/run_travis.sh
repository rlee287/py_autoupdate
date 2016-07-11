#!/bin/sh
# Run tests
echo -e "\e[0;34mRunning test suite...\e[0m"
cd 'test' || exit 1
coverage run --debug config --source .,../pyautoupdate -m pytest
test_exit=$?
coverage report -m
coverage xml -i
mv coverage.xml ../coverage.xml
cd ..
echo -e "\e[0;34mDone running tests\e[0m"
# Ensure that package installs properly
echo -e "\e[0;35mInstalling package...\e[0m"
python setup.py develop || exit 1
echo -e "\e[0;35mDone installing\e[0m"
echo -e "\e[0;35mAttempting to import package from python...\e[0m"
python -c "import pyautoupdate" && echo -e "\e[0;32mInstallation successful\e[0m"
install_exit=$?
echo -e "\e[0;35mCleaning up...\e[0m"
python setup.py develop --uninstall
if [ $test_exit = 0 ] && [ $install_exit = 0 ]; then
    exit 0
else
    exit 1
fi
