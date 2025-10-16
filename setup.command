#!/bin/bash

# Setup Script - Install all dependencies
# Double-click this file to set up the project

# 清屏
clear

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

echo "================================================"
echo "  Company Information API - Setup"
echo "================================================"
echo ""
echo "📂 项目目录: $SCRIPT_DIR"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda is not installed or not in PATH"
    echo ""
    echo "Please install Anaconda or Miniconda first:"
    echo "https://docs.conda.io/en/latest/miniconda.html"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✓ Conda found"
echo ""

# Source conda
source "$(conda info --base)/etc/profile.d/conda.sh"

# Check if environment already exists
if conda env list | grep -q "projAPI"; then
    echo "⚠️  projAPI 环境已存在"
    read -p "是否重新创建？(y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  删除现有环境..."
        conda env remove -n projAPI -y
    else
        echo "使用现有环境..."
        conda activate projAPI
        echo ""
        echo "📦 更新依赖..."
        pip install -r requirements_streamlit.txt
        echo ""
        echo "✅ 更新完成！"
        echo ""
        echo "下一步："
        echo "  • 双击 run_streamlit.command 启动仪表板"
        echo "  • 双击 run_flask.command 启动 API"
        echo ""
        read -p "按 Enter 键退出..."
        exit 0
    fi
fi

# Create conda environment
echo ""
echo "🔧 创建 projAPI 环境（Python 3.12）..."
conda create -n projAPI python=3.12 -y

if [ $? -ne 0 ]; then
    echo "❌ 创建环境失败"
    read -p "按 Enter 键退出..."
    exit 1
fi

echo "✅ 环境创建成功"
echo ""

# Activate environment
echo "🔧 激活环境..."
conda activate projAPI

# Install dependencies
echo "📦 安装依赖包..."
echo ""
pip install -r requirements_streamlit.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 安装依赖失败"
    read -p "按 Enter 键退出..."
    exit 1
fi

echo ""
echo "================================================"
echo "✅ 安装完成！"
echo "================================================"
echo ""
echo "已安装："
echo "  • Flask (REST API 框架)"
echo "  • Streamlit (仪表板框架)"
echo "  • yfinance (Yahoo Finance API)"
echo "  • pandas (数据处理)"
echo "  • 所有依赖包"
echo ""
echo "🚀 下一步："
echo ""
echo "  • 双击 run_streamlit.command  启动仪表板"
echo "    访问: http://localhost:8501"
echo ""
echo "  • 双击 run_flask.command  启动 API"
echo "    访问: http://localhost:5001"
echo ""
echo "  • 双击 run_tests.command  运行测试"
echo ""
echo "================================================"
echo ""
read -p "按 Enter 键退出..."
