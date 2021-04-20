@echo off

for /R %~dp0.. /D %%f in (*__pycache__) do ( 
echo %%f
rd /S /Q %%f
)
