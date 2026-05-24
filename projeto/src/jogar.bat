@echo off

start cmd /k "python server.py"

timeout /t 1 > nul

start cmd /k "python client.py"

timeout /t 1 > nul

start cmd /k "python client.py"
