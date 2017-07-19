pip list --outdated | grep -q pytest
if [ $? -eq 0 ]; then # match found
  echo "Upgrading pytest"
  pip install --upgrade pytest
else
  echo "Not upgrading pytest"
fi

