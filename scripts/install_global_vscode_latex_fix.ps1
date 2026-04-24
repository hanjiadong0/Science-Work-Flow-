param()

$ErrorActionPreference = "Stop"

$latexToolsRoot = Join-Path $env:LOCALAPPDATA "Programs\latex-tools"
$wrapperPath = Join-Path $latexToolsRoot "latexmk-global.cmd"
$strawberryRoot = Join-Path $env:LOCALAPPDATA "Programs\StrawberryPerl\Strawberry"
$fallbackStrawberryRoot = "C:\Strawberry"
$miktexBin = Join-Path $env:LOCALAPPDATA "Programs\MiKTeX\miktex\bin\x64"
$codeUserDir = Join-Path $env:APPDATA "Code\User"
$codeSettingsPath = Join-Path $codeUserDir "settings.json"
$codeCliPath = Join-Path $env:LOCALAPPDATA "Programs\Microsoft VS Code\bin\code.cmd"

if (-not (Test-Path (Join-Path $strawberryRoot "perl\bin\perl.exe")) -and -not (Test-Path (Join-Path $fallbackStrawberryRoot "perl\bin\perl.exe"))) {
    throw "Perl was not found. Expected Strawberry Perl under '$strawberryRoot' or '$fallbackStrawberryRoot'."
}

if (-not (Test-Path (Join-Path $miktexBin "latexmk.exe"))) {
    throw "MiKTeX latexmk.exe was not found under '$miktexBin'."
}

New-Item -ItemType Directory -Force -Path $latexToolsRoot | Out-Null
New-Item -ItemType Directory -Force -Path $codeUserDir | Out-Null

$wrapperContent = @'
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
'@

Set-Content -LiteralPath $wrapperPath -Value $wrapperContent -Encoding ASCII

function Add-PathEntries {
    param(
        [string[]]$Entries
    )

    $current = [Environment]::GetEnvironmentVariable("Path", "User")
    $parts = @()
    if ($current) {
        $parts = $current -split ";" | Where-Object { $_ -and $_.Trim() -ne "" }
    }

    for ($i = $Entries.Count - 1; $i -ge 0; $i--) {
        $entry = $Entries[$i]
        if ($parts -notcontains $entry) {
            $parts = @($entry) + $parts
        }
    }

    $newPath = ($parts | Select-Object -Unique) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    return $newPath
}

$activeStrawberryRoot = $strawberryRoot
if (-not (Test-Path (Join-Path $activeStrawberryRoot "perl\bin\perl.exe"))) {
    $activeStrawberryRoot = $fallbackStrawberryRoot
}

$updatedUserPath = Add-PathEntries @(
    $latexToolsRoot,
    (Join-Path $activeStrawberryRoot "c\bin"),
    (Join-Path $activeStrawberryRoot "perl\site\bin"),
    (Join-Path $activeStrawberryRoot "perl\bin")
)

$settingsObject = [pscustomobject]@{}
if (Test-Path $codeSettingsPath) {
    $rawSettings = Get-Content -LiteralPath $codeSettingsPath -Raw
    if ($rawSettings.Trim()) {
        $settingsObject = $rawSettings | ConvertFrom-Json
    }
}

function Set-Setting {
    param(
        [object]$Target,
        [string]$Name,
        [object]$Value
    )

    if ($Target.PSObject.Properties.Name -contains $Name) {
        $Target.$Name = $Value
    }
    else {
        $Target | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
    }
}

function Merge-ObjectSetting {
    param(
        [object]$Target,
        [string]$Name,
        [hashtable]$Entries
    )

    $merged = @{}
    if ($Target.PSObject.Properties.Name -contains $Name -and $Target.$Name) {
        $existing = $Target.$Name
        foreach ($prop in $existing.PSObject.Properties) {
            $merged[$prop.Name] = $prop.Value
        }
    }

    foreach ($key in $Entries.Keys) {
        $merged[$key] = $Entries[$key]
    }

    Set-Setting -Target $Target -Name $Name -Value ([pscustomobject]$merged)
}

$globalRecipes = @(
    [pscustomobject]@{
        name = "latexmk-global (pdfLaTeX)"
        tools = @("latexmk-global-pdf")
    },
    [pscustomobject]@{
        name = "latexmk-global (XeLaTeX)"
        tools = @("latexmk-global-xelatex")
    },
    [pscustomobject]@{
        name = "latexmk-global (LuaLaTeX)"
        tools = @("latexmk-global-lualatex")
    }
)

$globalTools = @(
    [pscustomobject]@{
        name = "latexmk-global-pdf"
        command = "cmd.exe"
        args = @(
            "/c",
            $wrapperPath,
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            "-outdir=%OUTDIR%",
            "%DOC%"
        )
        env = [pscustomobject]@{}
    },
    [pscustomobject]@{
        name = "latexmk-global-xelatex"
        command = "cmd.exe"
        args = @(
            "/c",
            $wrapperPath,
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-xelatex",
            "-outdir=%OUTDIR%",
            "%DOC%"
        )
        env = [pscustomobject]@{}
    },
    [pscustomobject]@{
        name = "latexmk-global-lualatex"
        command = "cmd.exe"
        args = @(
            "/c",
            $wrapperPath,
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-lualatex",
            "-outdir=%OUTDIR%",
            "%DOC%"
        )
        env = [pscustomobject]@{}
    }
)

Set-Setting -Target $settingsObject -Name "latex-workshop.latex.recipe.default" -Value "first"
Set-Setting -Target $settingsObject -Name "latex-workshop.view.pdf.viewer" -Value "tab"
Set-Setting -Target $settingsObject -Name "latex-workshop.latex.recipes" -Value $globalRecipes
Set-Setting -Target $settingsObject -Name "latex-workshop.latex.tools" -Value $globalTools
Set-Setting -Target $settingsObject -Name "latex-workshop.latex.clean.command" -Value "cmd.exe"
Set-Setting -Target $settingsObject -Name "latex-workshop.latex.clean.args" -Value @(
    "/c",
    $wrapperPath,
    "-outdir=%OUTDIR%",
    "-c",
    "%TEX%"
)
Merge-ObjectSetting -Target $settingsObject -Name "workbench.editorAssociations" -Entries @{
    "*.pdf" = "latex-workshop-pdf-hook"
}

$settingsJson = $settingsObject | ConvertTo-Json -Depth 20
Set-Content -LiteralPath $codeSettingsPath -Value $settingsJson -Encoding UTF8

$hasConflictingPdfExtension = $false
if (Test-Path $codeCliPath) {
    try {
        $installedExtensions = & $codeCliPath --list-extensions 2>$null
        $hasConflictingPdfExtension = $installedExtensions -contains "tomoki1207.pdf"
    }
    catch {
        $hasConflictingPdfExtension = $false
    }
}

Write-Host "Installed global LaTeX wrapper:"
Write-Host $wrapperPath
Write-Host ""
Write-Host "Updated VS Code user settings:"
Write-Host $codeSettingsPath
Write-Host ""
Write-Host "Updated user PATH:"
Write-Host $updatedUserPath
Write-Host ""
if ($hasConflictingPdfExtension) {
    Write-Host "VS Code still has the conflicting 'vscode-pdf' extension installed." -ForegroundColor Yellow
    Write-Host "To avoid PDF sidebar conflicts with LaTeX Workshop across repos, run:" -ForegroundColor Yellow
    Write-Host ('"{0}" --uninstall-extension tomoki1207.pdf' -f $codeCliPath) -ForegroundColor Yellow
    Write-Host ""
}
Write-Host "Reload VS Code for the new settings to apply."
