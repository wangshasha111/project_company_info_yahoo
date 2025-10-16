#!/bin/bash

# Run Streamlit Dashboard
# Double-click this file to start the Streamlit dashboard

# 清屏
clear

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

echo "================================================"
echo "  Company Information Dashboard - Streamlit"
echo "================================================"
echo ""
echo "📂 项目目录: $SCRIPT_DIR"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ 错误：找不到 conda"
    echo "请先安装 Anaconda 或 Miniconda"
    read -p "按 Enter 键退出..."
    exit 1
fi

# Source conda
echo "🔧 初始化 conda..."
CONDA_BASE=$(conda info --base)
if [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
    source "$CONDA_BASE/etc/profile.d/conda.sh"
else
    echo "❌ 无法初始化 conda"
    read -p "按 Enter 键退出..."
    exit 1
fi

# Check if environment exists
if ! conda env list | grep -q "projAPI"; then
    echo "❌ 错误：projAPI 环境不存在"
    echo ""
    echo "请先运行 setup.command 创建环境"
    read -p "按 Enter 键退出..."
    exit 1
fi

# Activate environment
echo "🔧 激活 projAPI 环境..."
conda activate projAPI

# Check if Streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ 错误：Streamlit 未安装"
    echo ""
    echo "正在安装依赖..."
    pip install -r requirements_streamlit.txt
fi

# Run the Streamlit app
echo ""
echo "🚀 启动 Streamlit 仪表板..."
echo ""
echo "📊 仪表板地址: http://localhost:8501"
echo ""
echo "⏳ 等待服务器启动..."
echo "🌐 浏览器将自动打开"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================================"
echo ""

# Run the app (Streamlit will automatically open browser with headless=false)
streamlit run streamlit_app.py

# Note: Browser opening is handled by Streamlit's built-in feature
# Configured in .streamlit/config.toml with headless=false

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 启动失败"
    read -p "按 Enter 键退出..."
fi
