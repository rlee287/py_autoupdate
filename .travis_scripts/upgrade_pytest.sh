pip list --outdated | grep -q pytest
if [ $? -eq 0 ]; then # match found
  pip install --upgrade pytest
fi
pip install --upgrade pytest

