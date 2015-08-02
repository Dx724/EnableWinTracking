# EnableWinTracking
Uses some known methods that attempt to disable tracking in Windows 10 to re-enable it

## Dependencies
* wxPython
* PyWin32
* Windows 10 (Duh)

## Methods Used
#### Telemetry
Set the "AllowTelemetry" string in "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\DataCollection" to 1

#### DiagTrack Log
Enables writing to the log located in "C:\ProgramData\Microsoft\Diagnosis\ETLLogs\AutoLogger"

#### Services
* Enable: Set the "Start" registry key for both services to 2 (Automatic) Located at "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\"

#### HOSTS
Reset the HOSTS file located in "C:\Windows\System32\drivers\etc"

## How to use
Install Python and the 2 dependencies and run the script from an elevated (admin) command prompt and select which options you'd like
