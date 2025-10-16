#!/bin/bash

# Run Flask API Server
# Double-click this file to start the Flask API

# 清屏
clear

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

echo "================================================"
echo "  Company Information API - Flask Server"
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

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ 错误：Flask 未安装"
    echo ""
    echo "正在安装依赖..."
    pip install -r requirements.txt
fi

# Run the Flask app
echo ""
echo "🚀 启动 Flask API 服务器..."
echo ""
echo "📡 API 地址："
echo "   http://localhost:5001"
echo "   http://localhost:5001/api/health"
echo "   http://localhost:5001/api/company/AAPL"
echo ""
echo "⏳ 等待服务器启动..."
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================================"
echo ""

# Start Flask in background to allow browser opening
python app.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 2

# Open browser to API documentation page
if command -v open &> /dev/null; then
    echo "🌐 正在打开浏览器..."
    open "http://localhost:5001"
fi

# Wait for Flask process
wait $FLASK_PID

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 启动失败"
    read -p "按 Enter 键退出..."
fi
