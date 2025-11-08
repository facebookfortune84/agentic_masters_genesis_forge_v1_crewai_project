$maxRetries = 10
$currentTry = 0
$waitTime = 20

do {
    $currentTry++
    Write-Host "=== ATTEMPT $currentTry of $maxRetries ===" -ForegroundColor Green
    Write-Host "Waiting $waitTime seconds for rate limit reset..." -ForegroundColor Yellow
    Start-Sleep $waitTime
    
    Write-Host "Starting Genesis Forge..." -ForegroundColor Cyan
    $result = & crewai run 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS! Genesis Forge completed!" -ForegroundColor Green
        exit 0
    }
    
    # Check if it's a rate limit error
    if ($result -match "rate_limit_exceeded|Rate limit reached") {
        Write-Host "Rate limit hit - will retry in $waitTime seconds..." -ForegroundColor Yellow
        $waitTime = [Math]::Min($waitTime * 1.5, 120)  # Exponential backoff, max 2 min
    } else {
        Write-Host "Non-rate-limit error encountered:" -ForegroundColor Red
        Write-Host $result
        exit 1
    }
    
} while ($currentTry -lt $maxRetries)

Write-Host "Max retries reached. Please check the configuration." -ForegroundColor Red
