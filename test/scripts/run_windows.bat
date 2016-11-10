@echo off
coverage run --parallel-mode --source 'test,pyautoupdate' -m pytest
coverage combine
coverage report -m
coverage erase
