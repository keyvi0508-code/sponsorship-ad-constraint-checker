# Run the locked 23-caption AI pilot from the user's own PowerShell session.
# If the session has no API key, prompt privately; never save or print it.
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
    python scripts/evaluate_public_captions.py --run-api --confirm-paid-run
    if ($LASTEXITCODE -ne 0) {
        throw "Caption AI run exited with code $LASTEXITCODE. Inspect reports/public_caption_ai_v1.jsonl if it exists."
    }
}
finally {
    if ($promptedForKey) {
        Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue
    }
}
