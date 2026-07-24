$pythonPath = "C:\Users\meyrr\AppData\Local\Programs\Python\Python312\python.exe"
$workingDir = "C:\Users\meyrr\.gemini\antigravity\scratch\onenote-media-briefing"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "main.py" -WorkingDirectory $workingDir
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "DailyOneNoteMediaBriefing" -Action $action -Trigger $trigger -Settings $settings -Force
Write-Host "Successfully registered Task 'DailyOneNoteMediaBriefing' to run daily at 8:00 AM!"
