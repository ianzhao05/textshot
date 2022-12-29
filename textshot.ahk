#NoEnv
SetWorkingDir %A_ScriptDir%

; Bind the script to Win + Ctrl + S; modify as needed
#^s::
; Run Python w/o a window in a virtual environment in .venv
; Modify the command as needed, e.g. if not using a virtual environment
Run, .\.venv\Scripts\textshotw.exe
Return
