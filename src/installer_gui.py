#!/usr/bin/env python3
"""自动安装程序 GUI - 使用 Tkinter 实现跨平台自动安装"""

import os
import platform
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from dataclasses import dataclass


@dataclass
class InstallerConfig:
    """安装配置类"""

    linux_mac_url: str = "https://gh-proxy.com/https://raw.githubusercontent.com/NMG-AI/autoRun/main/run.sh"
    windows_url: str = "https://gh-proxy.com/https://raw.githubusercontent.com/NMG-AI/autoRun/main/run.ps1"
    silent: bool = False


class AutoInstallerApp:
    """自动安装程序主类"""

    # 蓝色主题配色
    COLORS = {
        "bg_primary": "#2196F3",  # 主蓝色
        "bg_secondary": "#1976D2",  # 深蓝色
        "bg_dark": "#1565C0",  # 更深蓝色
        "bg_light": "#E3F2FD",  # 浅蓝色背景
        "bg_hover": "#42A5F5",  # 悬停蓝色
        "text_white": "#FFFFFF",
        "text_primary": "#1565C0",
        "text_success": "#2E7D32",
        "text_error": "#C62828",
        "text_info": "#1976D2",
    }

    def __init__(
        self, root: tk.Tk, config: InstallerConfig | None = None
    ) -> None:
        self.root = root
        self.root.title("自动安装程序")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS["bg_light"])

        self.config = config or InstallerConfig()

        # 按钮状态
        self.button_hover = False
        self.install_button = tk.Label(root, text="")  # 用于跟踪状态的隐藏控件

        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置用户界面"""
        # 顶部蓝色横幅
        header_frame = tk.Frame(self.root, bg=self.COLORS["bg_primary"], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🚀 自动安装程序",
            font=("Arial", 20, "bold"),
            bg=self.COLORS["bg_primary"],
            fg=self.COLORS["text_white"],
        )
        title_label.pack(pady=25)

        # 主内容区域
        main_frame = tk.Frame(self.root, bg=self.COLORS["bg_light"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        info_label = tk.Label(
            main_frame,
            text="点击下方按钮开始自动安装\n系统将自动下载并执行安装脚本",
            font=("Arial", 11),
            bg=self.COLORS["bg_light"],
            fg="#546E7A",
            justify=tk.CENTER,
        )
        info_label.pack(pady=(10, 30))

        # 安装按钮框架 - 使用圆角画布
        button_frame = tk.Frame(main_frame, bg=self.COLORS["bg_light"])
        button_frame.pack(pady=30)

        # 创建圆角按钮效果
        self.button_canvas = tk.Canvas(
            main_frame,
            width=220,
            height=60,
            bg=self.COLORS["bg_light"],
            highlightthickness=0,
            cursor="hand2",
        )
        self.button_canvas.pack()

        # 绘制圆角矩形按钮
        self._draw_button()

        # 绑定事件
        self.button_canvas.bind("<Button-1>", lambda e: self._start_installation())
        self.button_canvas.bind("<Enter>", self._on_button_hover)
        self.button_canvas.bind("<Leave>", self._on_button_leave)

        self.button_text_id = self.button_canvas.create_text(
            110,
            30,
            text="⬇️ 开始安装",
            font=("Arial", 16, "bold"),
            fill=self.COLORS["text_white"],
        )

        # 状态显示区域
        status_frame = tk.Frame(main_frame, bg=self.COLORS["bg_light"])
        status_frame.pack(pady=(30, 10))

        self.status_label = tk.Label(
            status_frame,
            text="⏳ 状态：等待开始",
            font=("Arial", 10),
            bg=self.COLORS["bg_light"],
            fg="#90A4AE",
        )
        self.status_label.pack()

        # 进度条
        self.progress_bar = ttk.Progressbar(
            main_frame,
            mode="indeterminate",
            length=380,
            style="blue.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(pady=(20, 0))

        # 配置进度条样式
        self.progress_bar["style"] = "blue.Horizontal.TProgressbar"
        ttk.Style().configure(
            "blue.Horizontal.TProgressbar",
            troughcolor="#BBDEFB",
            background=self.COLORS["bg_primary"],
        )

    def _draw_button(self, hover: bool = False) -> None:
        """绘制按钮"""
        self.button_canvas.delete("all")

        bg_color = self.COLORS["bg_hover"] if hover else self.COLORS["bg_primary"]

        width = 220
        height = 60

        # 绘制矩形
        self.button_canvas.create_rectangle(
            0, 0, width, height,
            fill=bg_color,
            outline="",
        )

        # 重新绘制文字和图标
        self.button_text_id = self.button_canvas.create_text(
            110,
            30,
            text="⬇️ 开始安装",
            font=("Arial", 16, "bold"),
            fill=self.COLORS["text_white"],
        )

    def _draw_button_disabled(self) -> None:
        """绘制禁用状态按钮"""
        self.button_canvas.delete("all")

        bg_color = "#90A4AE"  # 灰色
        radius = 30
        width = 220
        height = 60

        # 主体矩形
        self.button_canvas.create_rectangle(
            0, radius, width, height - radius,
            fill=bg_color,
            outline="",
        )

        # 上下半圆
        self.button_canvas.create_arc(
            0, 0, radius * 2, radius * 2,
            start=90, extent=180,
            fill=bg_color,
            outline="",
        )
        self.button_canvas.create_arc(
            width - radius * 2, 0, width, radius * 2,
            start=-90, extent=180,
            fill=bg_color,
            outline="",
        )
        self.button_canvas.create_arc(
            0, height - radius * 2, radius * 2, height,
            start=180, extent=180,
            fill=bg_color,
            outline="",
        )
        self.button_canvas.create_arc(
            width - radius * 2, height - radius * 2, width, height,
            start=0, extent=180,
            fill=bg_color,
            outline="",
        )

        # 绘制文字（使用淡色）
        self.button_text_id = self.button_canvas.create_text(
            110,
            30,
            text="⏳ 安装中...",
            font=("Arial", 16, "bold"),
            fill="#B3E5FC",
        )

    def _on_button_hover(self, event: tk.Event) -> None:
        """鼠标悬停效果"""
        if self.install_button.cget("state") != "disabled":
            self.button_hover = True
            self._draw_button(hover=True)

    def _on_button_leave(self, event: tk.Event) -> None:
        """鼠标离开效果"""
        if self.install_button.cget("state") != "disabled":
            self.button_hover = False
            self._draw_button(hover=False)

    def _get_install_command(self) -> list[str] | None:
        """根据操作系统获取安装命令"""
        system = platform.system()

        if system == "Windows":
            return [
                "powershell",
                "-Command",
                f"$ErrorActionPreference = 'Stop'; iwr -useb {self.config.windows_url} | iex",
            ]
        elif system in ("Linux", "Darwin"):
            return [
                "bash",
                "-c",
                f"set -e -o pipefail; curl -fsSL {self.config.linux_mac_url} | bash",
            ]
        else:
            return None

    def _run_installation(self, command: list[str]) -> bool:
        """执行安装脚本"""
        system = platform.system()

        if self.config.silent:
            # 静默模式：后台执行，不显示终端，但需等待结果
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300,
                )
                return result.returncode == 0
            except subprocess.TimeoutExpired:
                return False
            except Exception:
                return False
        else:
            # 非静默模式：打开新终端窗口执行，允许交互
            return self._run_in_new_terminal(command, system)

    def _run_in_new_terminal(self, command: list[str], system: str) -> bool:
        """在新终端窗口中运行命令，允许用户交互"""
        try:
            if system == "Windows":
                # Windows: 打开新 PowerShell 窗口执行
                # command 是 ["powershell", "-Command", "..."]，提取实际命令
                actual_command = " ".join(command[2:])  # 取 "iwr ... | iex"
                subprocess.Popen(
                    ["powershell", "-NoExit", "-Command", actual_command],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
                return True
            elif system == "Darwin":
                # macOS: 使用 Terminal.app 打开窗口执行脚本
                # 先将命令写入临时脚本文件，避免 AppleScript 转义问题
                import tempfile

                cmd_str = " ".join(command)

                # 创建临时脚本
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".sh", delete=False
                ) as f:
                    f.write("#!/bin/bash\n")
                    f.write(cmd_str + "\n")
                    script_path = f.name

                os.chmod(script_path, 0o755)

                # 使用多行 AppleScript，需要用多个 -e 参数
                result = subprocess.run(
                    [
                        "osascript",
                        "-e",
                        "tell application \"Terminal\"",
                        "-e",
                        "activate",
                        "-e",
                        f'do script "bash {script_path}"',
                        "-e",
                        "end tell",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                # 写入日志
                log_path = os.path.expanduser("~/auto_installer.log")
                with open(log_path, "a") as f:
                    f.write(f"osascript result: returncode={result.returncode}\n")
                    f.write(f"stdout: {result.stdout}\n")
                    f.write(f"stderr: {result.stderr}\n")
                    f.write(f"script_path: {script_path}\n")
                    f.write("---\n")

                return result.returncode == 0
            else:
                # Linux: 尝试多个终端模拟器
                terminals = [
                    ("gnome-terminal", ["--", "bash", "-c"]),
                    ("konsole", ["--hold", "-e"]),
                    ("xfce4-terminal", ["-e"]),
                    ("xterm", ["-e"]),
                    ("mate-terminal", ["-e"]),
                ]
                for terminal, args in terminals:
                    if shutil.which(terminal):
                        subprocess.Popen([terminal] + args + [" ".join(command)])
                        return True
                return False
            return True
        except Exception:
            return False

    def _start_installation(self) -> None:
        """开始安装流程"""
        # 禁用按钮
        self.install_button.config(state="disabled")
        self.button_canvas.itemconfig(
            self.button_text_id,
            text="⏳ 安装中...",
            fill="#B3E5FC",
        )
        self._draw_button_disabled()
        self.progress_bar.start()

        command = self._get_install_command()

        if not command:
            messagebox.showerror("错误", "不支持的操作系统")
            self._reset_ui()
            return

        # 根据 silent 配置更新状态提示
        if self.config.silent:
            self.status_label.config(text="🔄 状态：正在安装（后台）...", fg=self.COLORS["text_info"])
        else:
            self.status_label.config(text="🔄 状态：正在安装...", fg=self.COLORS["text_info"])

        try:
            success = self._run_installation(command)
        except subprocess.TimeoutExpired:
            self.status_label.config(text="❌ 状态：安装超时", fg=self.COLORS["text_error"])
            if self.config.silent:
                messagebox.showerror("❌ 错误", "安装超时，请检查网络连接")
            return
        except Exception as e:
            self.status_label.config(text="❌ 状态：安装失败", fg=self.COLORS["text_error"])
            if self.config.silent:
                messagebox.showerror("❌ 错误", f"发生错误：{str(e)}")
            return

        # 根据 silent 配置处理结果
        if self.config.silent:
            if success:
                self.status_label.config(
                    text="✅ 状态：安装成功！", fg=self.COLORS["text_success"]
                )
                messagebox.showinfo("✅ 成功", "安装完成！")
            else:
                self.status_label.config(
                    text="❌ 状态：安装失败", fg=self.COLORS["text_error"]
                )
                messagebox.showerror("❌ 错误", "安装脚本执行失败")
        else:
            # 非静默模式：已在终端中显示输出
            if success:
                self.status_label.config(
                    text="🚀 已在终端窗口中打开安装程序", fg=self.COLORS["text_info"]
                )
            else:
                self.status_label.config(
                    text="❌ 状态：无法打开终端窗口", fg=self.COLORS["text_error"]
                )
            self.progress_bar.stop()
            self.install_button.config(state="normal")
            self.button_canvas.itemconfig(
                self.button_text_id,
                text="⬇️ 开始安装",
                fill=self.COLORS["text_white"],
            )
            self._draw_button()

    def _reset_ui(self) -> None:
        """重置 UI 状态"""
        self.install_button.config(state="normal")
        self.progress_bar.stop()
        self.button_canvas.itemconfig(
            self.button_text_id,
            text="⬇️ 开始安装",
            fill=self.COLORS["text_white"],
        )
        self._draw_button()
        self.status_label.config(text="⏳ 状态：等待开始", fg="#90A4AE")


def main() -> None:
    """程序入口"""
    root = tk.Tk()

    # 创建配置对象
    config = InstallerConfig(
        linux_mac_url="https://gh-proxy.com/https://raw.githubusercontent.com/NMG-AI/autoRun/main/run.sh",
        windows_url="https://gh-proxy.com/https://raw.githubusercontent.com/NMG-AI/autoRun/main/run.ps1",
        silent=False,
    )

    app = AutoInstallerApp(root, config)

    root.mainloop()


if __name__ == "__main__":
    main()
