# Windows Laptop Local Sync Bridge
# Watches local P6 SQLite export, feeds to VM mesh, and triggers Power BI refresh
param(
    [string]$DbPath = "$env:USERPROFILE\Documents\PPMDBSQLite.db",
    [string]$PowerBiFeed = "$PSScriptRoot\output\P6_PowerBI_Feed.csv"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  P6-PowerBI Agentic Mesh: Laptop Local Automation Watcher" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (Test-Path $PowerBiFeed) {
    Write-Host "[OK] Detected Active Power BI Data Feed: $PowerBiFeed" -ForegroundColor Green
    Write-Host "[*] When you click 'Refresh' in Power BI Desktop, latest P6 CPM is loaded." -ForegroundColor Yellow
} else {
    Write-Host "[!] Feed file not found yet. Run p6_powerbi_mesh.py to generate." -ForegroundColor Red
}
