#!/bin/bash
trap ctrl_c INT

ctrl_c ()
{
    if [ -d "$tempclone" ]; then
        rm -rf "$tempclone"
    fi
    if [ "$pushdired" -eq 1 ]; then
        popd > /dev/null
    fi
}


tempclone=$(mktemp -d "/tmp/doc_build_clone.XXXXXXXX")
#if [ ! -d "docs/build/html" ]; then
#    echo -e "\e[0;31mDocumentation is not built\e[0m"
echo "Building documentation"
cd docs
make html
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
SHA=`git rev-parse --short --verify HEAD`
BRANCH=`git rev-parse --abbrev-ref HEAD`
#fi
cd docs/build/html
builtdocs=$PWD
cd ../../..
echo $builtdocs
pushd $tempclone > /dev/null
if [ $? -ne 0 ]; then
    echo -e "\e[0;31mFailed to use temp directory\e[0m"
    ctrl_c
    exit 1
fi
pushdired=1
git clone --depth 1 -b gh-pages git@github.com:rlee287/pyautoupdate
if [ $? -ne 0 ]; then
    echo -e "\e[0;31mFailed to clone current gh-pages repo\e[0m"
    ctrl_c
    exit 1
fi
cd pyautoupdate
#ls -a --color
git ls-files | xargs rm
shopt -u | grep -q dotglob && changed=true && shopt -s dotglob
cp -r $builtdocs/* .
[ $changed ] && shopt -u dotglob; unset changed
#cp -rv $builtdocs .
#echo "test"
#mv -v 'html' ..
# Keep some of the existing indicator files
git checkout -- .nojekyll
git checkout -- .gitignore
# This step is necessary on Windows Cygwin
# Or other systems that do not handle executable bits properly
chmod -x *
chmod -x **/*
git config --local core.fileMode true
git diff --stat
#git diff --staged > /tmp/docbuild.patch
if [ "$TRAVIS" = "true" ]; then
  # Running on Travis CI Server
  git config --local user.name TravisCIDocBuild
  git config --local user.email travis_build@nonexistent.email
fi
echo "Checking for changed documentation"
git diff --quiet
hasdiff=$?
if [ $hasdiff -eq 0 ]; then
    echo "Documentation has not changed"
    echo "No need to update"
    exit 0
fi
if [ "$TRAVIS" = "true" ]; then
  # Running on Travis CI Server
  echo "Running on Travis CI Server"
  if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
      echo "Skipping deployment of doc on Pull Request build"
      exit 0
  fi
  git config --local user.name TravisCIDocBuild
  git config --local user.email travis_build@nonexistent.email
else
  echo "Running locally"
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
if [ $DOCBUILD == true ] && [ $TRAVIS == true]; then
  # Decrypt server SSH key
  openssl aes-256-cbc -K $encrypted_17ecf7cd0287_key -iv $encrypted_17ecf7cd0287_iv -in sphinx_travis_deploy.enc -out sphinx_travis_deploy -d
  if [ -f sphinx_travis_deploy ]; then
    chmod 600 sphinx_travis_deploy
    eval `ssh-agent -s`
    ssh-add sphinx_travis_deploy
    echo "Pushing to gh-pages"
    git push
    eval `ssh-agent -k`
  else
    echo -e "\e[0;31mFailed to decrypt deploy key\e[0m"
  fi
else
  # Assume local users have proper authentication in place
  git push
fi
ctrl_c
