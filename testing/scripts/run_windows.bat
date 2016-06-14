@echo off
cd testing
if errorlevel 0 (
    py.test .
    cd ..
)
