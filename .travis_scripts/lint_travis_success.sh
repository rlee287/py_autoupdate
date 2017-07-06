if [ ! -z "$PYLINT" ]; then
  pip install pylint
  cd ..
  pylint -f colorized pyautoupdate
  cd pyautoupdate
fi
