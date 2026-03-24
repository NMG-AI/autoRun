#!/bin/bash

set -e

echo "开始安装..."

# 创建示例应用
cat > hello.py << 'EOF'
#!/usr/bin/env python3
print("Hello World")
EOF

chmod +x hello.py

echo "安装完成！"
echo "运行 python3 hello.py 测试"
