@echo off
cd test
if errorlevel 0 (
    py.test .
    cd ..
)
