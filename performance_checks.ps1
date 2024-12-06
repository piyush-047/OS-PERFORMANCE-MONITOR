# performance_checks.ps1

Write-Host "Starting advanced system checks..."

# Check running services
Write-Host "Checking critical services..."
Get-Service | Where-Object {$_.Status -eq "Stopped"} | Export-Csv -Path stopped_services.csv -NoTypeInformation
Write-Host "Stopped services logged to stopped_services.csv."

# Check network status
Write-Host "Checking network connectivity..."
Test-Connection -ComputerName "8.8.8.8" -Count 4 | Export-Csv -Path network_status.csv -NoTypeInformation
Write-Host "Network status logged to network_status.csv."

# Collect Event Viewer logs
Write-Host "Collecting Event Viewer logs..."
Get-EventLog -LogName System -Newest 1000 | Export-Csv -Path system_logs.csv -NoTypeInformation
Write-Host "System logs saved to system_logs.csv."

