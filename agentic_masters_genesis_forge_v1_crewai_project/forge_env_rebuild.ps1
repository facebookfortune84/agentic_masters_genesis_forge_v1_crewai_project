# =====================================================================
# 💎 REALMS TO RICHES | AGENTIC MASTER FORGE™
# ENVIRONMENT REBUILD SCRIPT (PowerShell, 2025)
# ---------------------------------------------------------------------
# Cleans all virtual/conda environments and builds a clean .venv
# using Python 3.11 installed on PATH (safe for external drives).
# =====================================================================

Write-Host "`n🧹 Cleaning Forge Environment..." -ForegroundColor Cyan
Set-Location -Path (Get-Location).Path

# 1️⃣ Deactivate any active envs
try { deactivate 2>$null } catch {}
try { conda deactivate 2>$null } catch {}

# 2️⃣ Remove local .venv or forge_env folders
Get-ChildItem -Directory -Filter ".venv" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "🗑️  Removing: $($_.FullName)" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $_.FullName
}

Get-ChildItem -Directory -Filter "forge_env" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "🗑️  Removing: $($_.FullName)" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $_.FullName
}

# 3️⃣ Delete Conda environment if exists
try {
    $condaEnvList = conda info --envs 2>$null
    if ($condaEnvList -match "genesis_forge_env") {
        Write-Host "🗑️  Deleting Conda env: genesis_forge_env" -ForegroundColor Yellow
        conda env remove -n genesis_forge_env -y
    }
} catch {
    Write-Host "⚠️  Conda not detected, skipping..." -ForegroundColor DarkGray
}

# 4️⃣ Locate Python 3.11
Write-Host "`n🐍 Checking for Python 3.11..." -ForegroundColor Cyan
$pythonPaths = & where.exe python 2>$null | ForEach-Object { $_.Trim() }

if (-not $pythonPaths) {
    Write-Host "❌ No Python found on PATH. Install Python 3.11 from python.org." -ForegroundColor Red
    exit 1
}

$python311 = $pythonPaths | Where-Object { $_ -match "Python311" }

if (-not $python311) {
    Write-Host "⚠️ Python 3.11 not found — using first available interpreter." -ForegroundColor Yellow
    $python311 = $pythonPaths[0]
}

Write-Host "✅ Using Python: $python311" -ForegroundColor Green

# 5️⃣ Create new .venv
Write-Host "`n⚙️  Creating clean .venv ..." -ForegroundColor Cyan
& "$python311" -m venv .venv

if (-not (Test-Path ".\.venv\Scripts\activate")) {
    Write-Host "❌ Failed to create .venv. Aborting." -ForegroundColor Red
    exit 1
}

# 6️⃣ Activate venv
& .\.venv\Scripts\activate
Write-Host "✅ Virtual environment activated." -ForegroundColor Green

# 7️⃣ Upgrade base tools
Write-Host "`n⬆️  Upgrading pip/setuptools/wheel..." -ForegroundColor Cyan
pip install --upgrade pip setuptools wheel

# 8️⃣ Install dependencies
if (Test-Path "pyproject.toml") {
    Write-Host "`n📦 Installing dependencies from pyproject.toml ..." -ForegroundColor Cyan
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv pip install -e . --all-extras
    } elif {
        pip install .[all]
    } else {
        Write-Host "`n⚠️ pyproject.toml not found — installing core dependencies manually" -ForegroundColor Yellow
        pip install moviepy opencv-python pydub colorama requests simpleaudio python-dotenv tqdm imageio[ffmpeg]
    }
}

# 9️⃣ Verify core imports
Write-Host "`n🧠 Verifying critical modules..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe -c "import moviepy.editor, cv2, pydub; print('✅ Forge dependencies OK')"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Import check failed. Some modules missing." -ForegroundColor Red
    exit 1
}

# 🔟 Display environment info
Write-Host "`n🔎 Environment verification..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe -m site

Write-Host "`n🌟 Forge environment rebuilt successfully!"
Write-Host "Activate anytime with: .\.venv\Scripts\activate`n" -ForegroundColor Green"