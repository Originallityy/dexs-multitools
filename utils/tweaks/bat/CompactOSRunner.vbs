' filepath: /c:/Users/origi/Desktop/what the sigm/utils/RunCompactOS.vbs
Set objShell = CreateObject("Shell.Application")
' Get the script's directory
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
' Execute the BAT file with elevated privileges
objShell.ShellExecute "cmd.exe", "/c """ & strPath & "\CompactOS.bat""", "", "runas", 1
