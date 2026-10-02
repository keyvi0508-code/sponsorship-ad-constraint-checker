# Run the locked exploratory one-stage comparison in the user's PowerShell.
# The API key is prompted privately if absent; it is never printed or saved.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$promptedForKey = $false

try {
    Set-Location -LiteralPath $projectRoot
    if (-not $env:OPENROUTER_API_KEY -and -not $env:OPENAI_API_KEY) {
        $secureKey = Read-Host 'OpenRouter API key (input hidden)' -AsSecureString
        $keyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
        try {
            $env:OPENROUTER_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPointer)
            $promptedForKey = $true
        }
        finally {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPointer)
            Remove-Variable secureKey -ErrorAction SilentlyContinue
        }
    }
    python scripts/evaluate_single_stage_ablation.py --run-api --confirm-paid-run
    if ($LASTEXITCODE -ne 0) {
        throw "Ablation exited with code $LASTEXITCODE. Inspect reports/single_stage_ablation_extension_v2.jsonl if it exists."
    }
}
finally {
    if ($promptedForKey) {
        Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue
    }
}
