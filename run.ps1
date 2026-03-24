# -*- coding: utf-8 -*-
Write-Host "开始安装..." -ForegroundColor Green

# 创建示例应用
$helloContent = @'
#!/usr/bin/env python3
print("Hello World")
'@

Set-Content -Path "hello.py" -Value $helloContent -Encoding UTF8

Write-Host "安装完成！" -ForegroundColor Green
Write-Host "运行 python hello.py 测试" -ForegroundColor Cyan
