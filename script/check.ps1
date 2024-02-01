$url = "http://aliyun.com/api/register"
$data = @{name="pc1"}

while ($true) {
    $response = Invoke-RestMethod -Uri $url -Method Post -Body ($data | ConvertTo-Json) -ContentType "application/json"

    if ($response -match "restart") {
        Write-Host "Received 'restart' signal. Restarting computer..."
        Restart-Computer
    }

    if ($response -match "shutdown") {
        Write-Host "Received 'shutdown' signal. Shutdown computer..."
        Stop-Computer
    }

    Start-Sleep -Seconds (10 * 60)  # 等待一定时间后再次发送请求
}
