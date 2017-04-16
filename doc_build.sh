#!/bin/bash
trap ctrl_c INT

ctrl_c ()
{
    if [ -d "$tempclone" ]; then
        rm -rf "$tempclone"
    fi
    if [ "$pushdired" = true ]; then
        popd > /dev/null
    fi
}
BUILD=true
PUSH=false
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    --no-build)
    BUILD=false
    ;;
    --push)
    PUSH=true
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done
if [ $BUILD = false ] && [ $PUSH = false ]; then
  echo "Error: Not building and not pushing"
  echo "At least one of these actions must be performed"
  ctrl_c
  exit 1
fi
tempclone=$(mktemp -d "doc_build_clone.XXXXXXXX")
echo $tempclone
if [ $PUSH = false ]; then
  echo "Only verification will be performed."
fi
if [ $BUILD = true ]; then
  echo "Building documentation"
  cd docs
  sphinx-build -b html -d build/doctrees source build/html
  makestatus=$?
  cd ..
else
  echo "Using previously built documentation"
  makestatus=0
fi
if [ $makestatus -ne 0 ]; then
  echo -e "\e[0;31mDocumentation building failed\e[0m"
  if [ ! -d "docs/build/html" ]; then
    echo -e "\e[0;31mDocumentation is not built\e[0m"
    ctrl_c
    exit 1
  else
    echo -e "\e[0;31mUsing previously built documentation\e[0m"
  fi
else
  echo -e "\e[0;32mDocumentation successfully built\e[0m"
fi
SHA=$(git rev-parse --short --verify HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ $PUSH = false ]; then
  echo "Exiting after doc verification"
  ctrl_c
  exit 0
fi
cd docs/build/html
builtdocs=$PWD
cd ../../..
pushd "$tempclone" > /dev/null
if [ $? -ne 0 ]; then
    echo -e "\e[0;31mFailed to use temp directory\e[0m"
    ctrl_c
    exit 1
fi
pushdired=true
# When running locally, use https as it is easier to configure
url=https://github.com/rlee287/pyautoupdate
git clone --depth 1 -b gh-pages $url
if [ $? -ne 0 ]; then
    echo -e "\e[0;31mFailed to clone current gh-pages repo\e[0m"
    ctrl_c
    exit 1
fi
cd pyautoupdate
git ls-files | xargs rm
shopt -u | grep -q dotglob && changed=true && shopt -s dotglob
cp --no-preserve=mode --no-preserve=ownership -r $builtdocs/* .
[ $changed ] && shopt -u dotglob; unset changed
# Keep some of the existing indicator files
git checkout -- .nojekyll
git checkout -- .gitignore
# This step is necessary on Windows Cygwin
# Or other systems that do not handle executable bits properly
chmod -x ./*
chmod -x ./**/*
git config --local core.fileMode true
git diff --stat
echo "Checking for changed documentation"
git diff --quiet
hasdiff=$?
if [ $hasdiff -eq 0 ]; then
    echo "Documentation has not changed"
    echo "No need to update"
    ctrl_c
    exit 0
fi
cat << EOF > commitmessage
Sphinx rebuild

This corresponds to commit $SHA on branch $BRANCH
EOF
echo "Committing updated documentation"
git add --all
git reset HEAD commitmessage
git diff --staged --stat
git commit -F commitmessage
rm commitmessage
echo "Pushing to gh-pages"
git push
ctrl_c
