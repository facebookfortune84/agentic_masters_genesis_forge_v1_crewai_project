# Forge Restructure Script — Robert's Agentic Master Forge

$packageFolder = "agentic_masters_genesis_forge_v1_crewai_project"
$initFile = "$packageFolder\__init__.py"
$uiInitFile = "ui\__init__.py"
$gitignoreFile = ".gitignore"

# Step 1: Create package folder if missing
if (-not (Test-Path $packageFolder)) {
    New-Item -ItemType Directory -Path $packageFolder | Out-Null
    Write-Host "Created package folder: $packageFolder"
}

# Step 2: Move core files into package folder
$coreFiles = @(
    "main.py",
    "crew.py",
    "forge_cloner.py",
    "forge_diagnostic.py",
    "inject_config.py",
    "inject_env_and_pyproject.py",
    "validate_forge.py",
    "validate_yaml.py",
    "multi_team_initializer.py"
)

foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        Move-Item $file $packageFolder
        Write-Host "Moved: $file → $packageFolder"
    }
    else {
        Write-Host "Missing: $file"
    }
}

# Step 3: Add __init__.py files
foreach ($init in @($initFile, $uiInitFile)) {
    if (-not (Test-Path $init)) {
        New-Item -ItemType File -Path $init | Out-Null
        Write-Host "Added: $init"
    }
}

# Step 4: Update .gitignore
$ignoreEntries = @(
    "__pycache__/",
    ".env",
    "secrets.toml",
    "*.log",
    ".vscode/",
    ".idea/",
    ".DS_Store"
)

if (-not (Test-Path $gitignoreFile)) {
    New-Item -ItemType File -Path $gitignoreFile | Out-Null
}

$existingIgnore = Get-Content $gitignoreFile
$updatedIgnore = $existingIgnore + ($ignoreEntries | Where-Object { $_ -notin $existingIgnore })
$updatedIgnore | Set-Content $gitignoreFile
Write-Host "Updated .gitignore"

# Final banner
Write-Host "`n🎉 Agentic Master Forge restructured and ready for launch!"
Write-Host "Package folder: $packageFolder"
Write-Host "Streamlit entry: ui/launch_ui.py"
Write-Host "Secrets excluded: .env, secrets.toml"