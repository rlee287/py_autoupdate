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
    if [ "$DOCBUILD" = true ] && [ "$TRAVIS" = true ]; then
      eval $(ssh-agent -k)
    fi
}

tempclone=$(mktemp -p . -d "doc_build_clone.XXXXXXXX")
echo $tempclone
if [ "$DOCBUILD" != true ]; then
  echo "Only verification will be performed."
fi
echo "Building documentation"
cd docs
sphinx-build -b html -d build/doctrees source build/html
makestatus=$?
cd ..
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
if [ "$DOCBUILD" != true ]; then
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
if [ "$DOCBUILD" = true ]; then
  echo "Decrypting SSH key"
  openssl aes-256-cbc -K $encrypted_17ecf7cd0287_key -iv $encrypted_17ecf7cd0287_iv -in $builtdocs/../../../sphinx_travis_deploy.enc -out sphinx_travis_deploy -d
    if [ -f sphinx_travis_deploy ] && [ -s sphinx_travis_deploy ]; then
      chmod 600 sphinx_travis_deploy
      eval $(ssh-agent -s)
      ssh-add sphinx_travis_deploy
      url=git@github.com:rlee287/pyautoupdate
    else
      echo -e "\e[0;31mFailed to decrypt deploy key\e[0m"
      url=https://github.com/rlee287/pyautoupdate
    fi
else
  # When running locally, use https as it is easier to configure
  url=https://github.com/rlee287/pyautoupdate
fi
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
git config --local core.fileMode true
git diff --stat
# Running on Travis CI Server
git config --local user.name TravisCIDocBuild
git config --local user.email travis_build@nonexistent.email
echo "Checking for changed documentation"
git diff --quiet
hasdiff=$?
if [ $hasdiff -eq 0 ]; then
    echo "Documentation has not changed"
    echo "No need to update"
    ctrl_c
    exit 0
fi
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "Skipping deployment of doc on Pull Request build"
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
