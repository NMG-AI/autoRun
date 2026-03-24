# autoRun - 跨平台自动安装程序

基于 Tkinter 的跨平台自动安装 GUI 程序。

## 功能

- 🖥️ 支持 Windows、Linux、macOS
- 🚀 一键自动安装
- 📦 简洁的图形界面

## 快速开始

### 运行 GUI 程序

```bash
python src/installer_gui.py
```

### 手动执行安装脚本

**Linux/macOS:**
```bash
curl -fsSL https://gh-proxy.com/https://raw.githubusercontent.com/NMG-AI/autoRun/main/run.sh | bash
```

**Windows:**
```powershell
iwr -useb https://gh-proxy.com/https://raw.githubusercontent.com/NMG-AI/autoRun/main/run.ps1 | iex
```

## 项目结构

```
autoRun/
├── src/
│   └── installer_gui.py    # Tkinter GUI 主程序
├── run.sh                   # Linux/macOS 安装脚本
├── run.ps1                  # Windows 安装脚本
├── pyproject.toml          # 项目配置
├── autoRun.spec            # PyInstaller 配置文件
├── requirements-build.txt  # 构建依赖
└── README.md               # 说明文档
```

## 自定义安装

修改 `run.sh` 和 `run.ps1` 文件来定制安装逻辑。

修改 `src/installer_gui.py` 中的 URL 地址（第 67 行）来指向你的安装脚本。

## 构建打包

### 本地构建

```bash
# 安装构建依赖
pip install -r requirements-build.txt

# 构建可执行文件
pyinstaller --noconfirm autoRun.spec
```

构建产物位于 `dist/autoRun` 目录。

### GitHub Actions 自动发布

推送 tag（如 v1.0.0）时会自动触发跨平台构建：

```bash
# 推送 tag 触发自动构建发布
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions 会在 Windows、macOS、Linux 上分别构建，并发布到 GitHub Releases。
