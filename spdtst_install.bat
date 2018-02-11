@echo off
echo Sugarloaf Speedtest Monitor Installer
echo Batch script edition

powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe', 'pyinstall.exe')"
rem downloads python 3.6.4 full installer

echo installing Python 3 and script prerequisites
pyinstall.exe PrependPath=1 /quiet
rem installs python 3.6.4, adds to windows path variable, without popping up UI

cd %HOMEPATH%\AppData\Local\Programs\Python\Python36
python -m pip install pymysql
python -m pip install speedtest-cli

cd %HOMEPATH%\Downloads
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/billionthb/sns-speedtest/master/spdtstdb.py', 'spdtstdb.py')"

mkdir C:\AUTORUN
cd C:\AUTORUN
set /p location="Enter Test Location Name: "
set /p ip="Enter Database IP address: "
set /p id="Enter Database username: "
set /p pw="Enter Database password: "
set /p db="Enter Database name: "
set /p tb="Enter Database table: "
rem to hard code any of the above, simply remove the /p flag and change the prompt to desired value

>speedtest.bat (
	echo python %HOMEPATH%\Downloads\spdtstdb.py "%location%" %ip% %id% %pw% %db% %tb%
)

rem set /p rep="How long is the test interval, in minutes: "
echo Now creating task to run speedtest automatically.
echo This will run under current user, and will ask for account password
echo If current user does not have ADMIN privileges, this may not work
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://drive.google.com/uc?export=download&id=1OmnGG13uVe5Vz3XsvnxxG5j9K5oPTw5q', 'speedtest.xml')"
rem schtasks /create /RU SYSTEM /SC ONSTART /TN Speedtest /TR C:/AUTORUN/speedtest.bat /RI %rep% /RL HIGHEST /F
schtasks /create /TN speedtest /RU %USERNAME% /XML speedtest.xml