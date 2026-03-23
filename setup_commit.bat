@echo off
echo Setting up automatic commit messages for Fishing Macro...
git config core.editor "python commit_hook.py"
echo.
echo Commit template configured to use Python hook
echo.
echo Now when you commit, it will automatically generate "Fishing Macro update" messages
echo.
pause
