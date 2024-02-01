@echo off
set URL=http://aliyun.com/api/register
set DATA={"name": "pc1"}

:LOOP
powershell -Command "$response = Invoke-RestMethod -Uri '%URL%' -Method Post -Body '%DATA%' -ContentType 'application/json';" ^
    "if ($response -match 'restart') {" ^
    "    Write-Host 'Received ''restart'' signal. Restarting computer...';" ^
    "    Restart-Computer" ^
    "} elseif ($response -match 'shutdown') {" ^
    "    Write-Host 'Received ''shutdown'' signal. Shutting down computer...';" ^
    "    Stop-Computer" ^
    "}"
timeout /t 600 >nul 2>nul
goto LOOP
