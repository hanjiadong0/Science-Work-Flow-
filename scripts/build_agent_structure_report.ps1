param(
    [string]$TexPath = "docs\cmbagent_opengauss_agent_structure_report.tex"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$resolvedTexPath = Join-Path $repoRoot $TexPath

if (-not (Test-Path -LiteralPath $resolvedTexPath)) {
    throw "TeX file not found: $resolvedTexPath"
}

$perlCommand = Get-Command perl -ErrorAction SilentlyContinue
if (-not $perlCommand) {
    $perlRootCandidates = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\StrawberryPerl\Strawberry'),
        'C:\Strawberry'
    )

    foreach ($perlRoot in $perlRootCandidates) {
        $perlExe = Join-Path $perlRoot 'perl\bin\perl.exe'
        if (Test-Path -LiteralPath $perlExe) {
            $prepend = @(
                (Join-Path $perlRoot 'c\bin'),
                (Join-Path $perlRoot 'perl\site\bin'),
                (Join-Path $perlRoot 'perl\bin')
            ) -join ';'
            $env:Path = "$prepend;$env:Path"
            $perlCommand = Get-Command perl -ErrorAction SilentlyContinue
            break
        }
    }
}

$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
if (-not $pdflatex) {
    throw "pdflatex was not found. Install MiKTeX/TeX and make sure pdflatex is on PATH."
}

$latexmk = Get-Command latexmk -ErrorAction SilentlyContinue
$outputDirectory = Split-Path -Parent $resolvedTexPath
$pdfPath = Join-Path $outputDirectory (([System.IO.Path]::GetFileNameWithoutExtension($resolvedTexPath)) + ".pdf")

Push-Location $repoRoot
try {
    if ($latexmk -and $perlCommand) {
        Write-Host "Running latexmk..."
        $previousPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            $latexOutput = & $latexmk.Source `
                "-pdf" `
                "-interaction=nonstopmode" `
                "-outdir=$outputDirectory" `
                $resolvedTexPath 2>&1
        }
        finally {
            $ErrorActionPreference = $previousPreference
        }

        $exitCode = $LASTEXITCODE
        $latexOutput | ForEach-Object { Write-Host $_ }

        if ($exitCode -ne 0) {
            $latexText = ($latexOutput | Out-String)
            $advice = ""
            if ($latexText -match "MiKTeX" -and ($latexText -match "neue TeX-Installation|Setup fertig|Updates gesucht|check for updates")) {
                $advice = " MiKTeX still needs first-run setup. Open MiKTeX Console once, finish setup/check updates, then rerun this script."
            }
            throw "latexmk failed.$advice"
        }
    }
    else {
        foreach ($pass in 1..2) {
            Write-Host "Running pdflatex pass $pass..."
            $previousPreference = $ErrorActionPreference
            $ErrorActionPreference = "Continue"
            try {
                $latexOutput = & $pdflatex.Source `
                    "-interaction=nonstopmode" `
                    "-halt-on-error" `
                    "-output-directory" $outputDirectory `
                    $resolvedTexPath 2>&1
            }
            finally {
                $ErrorActionPreference = $previousPreference
            }

            $exitCode = $LASTEXITCODE
            $latexOutput | ForEach-Object { Write-Host $_ }

            if ($exitCode -ne 0) {
                $latexText = ($latexOutput | Out-String)
                $advice = ""
                if ($latexText -match "MiKTeX" -and ($latexText -match "neue TeX-Installation|Setup fertig|Updates gesucht|check for updates")) {
                    $advice = " MiKTeX still needs first-run setup. Open MiKTeX Console once, finish setup/check updates, then rerun this script."
                }
                throw "pdflatex failed on pass $pass.$advice"
            }
        }
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "PDF built successfully:"
Write-Host $pdfPath
