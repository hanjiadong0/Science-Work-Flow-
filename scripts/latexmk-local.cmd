@echo off
setlocal

set "SP_ROOT=%LOCALAPPDATA%\Programs\StrawberryPerl\Strawberry"
if not exist "%SP_ROOT%\perl\bin\perl.exe" (
  set "SP_ROOT=C:\Strawberry"
)

set "MIKTEX_BIN=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64"

if not exist "%SP_ROOT%\perl\bin\perl.exe" (
  echo Perl not found. Expected either "%LOCALAPPDATA%\Programs\StrawberryPerl\Strawberry\perl\bin\perl.exe" or "C:\Strawberry\perl\bin\perl.exe".
  exit /b 1
)

if not exist "%MIKTEX_BIN%\latexmk.exe" (
  echo MiKTeX latexmk not found at "%MIKTEX_BIN%\latexmk.exe".
  exit /b 1
)

set "PATH=%SP_ROOT%\c\bin;%SP_ROOT%\perl\site\bin;%SP_ROOT%\perl\bin;%MIKTEX_BIN%;%PATH%"

"%MIKTEX_BIN%\latexmk.exe" %*
exit /b %ERRORLEVEL%
