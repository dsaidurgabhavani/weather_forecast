@echo off
title WeatherScope Launcher
echo ========================================================
echo        Starting WeatherScope Forecast Website...
echo ========================================================
echo.

cd /d "%~dp0"

set "STREAMLIT_EXE=%LOCALAPPDATA%\Programs\Python\Python311\Scripts\streamlit.exe"

if exist "%STREAMLIT_EXE%" (
    echo Launching with Python 3.11 Streamlit...
    "%STREAMLIT_EXE%" run app.py
) else (
    echo Launching with default streamlit...
    streamlit run app.py
)

pause
