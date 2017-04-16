#!/bin/sh
# Run tests
echo -e "\e[0;34mRunning test suite...\e[0m"
coverage run --debug config --parallel-mode --source 'test,pyautoupdate' -m pytest
test_exit=$?
echo -e "\e[0;34mDone running tests\e[0m"
echo -e "\e[0;34mReporting Coverage\e[0m"
coverage combine
coverage report -m
coverage xml -i
# Ensure that package installs properly
echo -e "\e[0;35mInstalling package...\e[0m"
python setup.py develop || exit 1
initialize_exit=1
echo -e "\e[0;35mDone installing\e[0m"
echo -e "\e[0;34mAttempting to import package from python...\e[0m"
python -c "import pyautoupdate" && echo -e "\e[0;32mImport successful\e[0m" || echo -e "\e[0;31mImport failed\e[0m"
install_exit=$?
if [ $install_exit = 0 ]; then
    echo -e "\e[0;34mInitializing launcher instance\e[0m"
    python -c "from pyautoupdate.launcher import Launcher;q=Launcher('file.py','URL')" \
        && echo -e "\e[0;32mInitialization successful\e[0m" || echo -e "\e[0;31mInitialization failed\e[0m"
echo -e "\e[0;35mCleaning up...\e[0m"
    initialize_exit=$?
fi
python setup.py develop --uninstall
if [ $test_exit = 0 ] && [ $install_exit = 0 ] && [ $initialize_exit = 0 ]; then
    exit 0
else
    exit 1
fi
