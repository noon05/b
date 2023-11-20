@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 0 /f