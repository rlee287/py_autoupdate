pip list --outdated > temp_pip_outdated.txt
grep -q pytest temp_pip_outdated.txt
if [ $? -eq 0 ]; then # match found
  echo "Upgrading pytest"
  pip install --upgrade pytest
else
  echo "Not upgrading pytest"
fi
rm temp_pip_outdated.txt

