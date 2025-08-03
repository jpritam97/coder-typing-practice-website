@echo off
echo Installing authentication dependencies...
echo =====================================
echo.
python check_requirements.py
echo.
echo Authentication system setup complete!
echo.
echo To start the server with authentication:
echo python server.py
echo.
pause 