#!/bin/bash

# Run API Tests
# Double-click this file to test the Flask API

# 清屏
clear

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

echo "================================================"
echo "  Company Information API - Test Suite"
echo "================================================"
echo ""
echo "📂 项目目录: $SCRIPT_DIR"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ 错误：找不到 conda"
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
    echo "请先运行 setup.command"
    read -p "按 Enter 键退出..."
    exit 1
fi

# Activate environment
echo "🔧 激活 projAPI 环境..."
conda activate projAPI

# Check if Flask API is running
echo "🔍 检查 Flask API 是否运行..."
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    echo "✅ Flask API 正在运行"
    echo ""
else
    echo "⚠️  Flask API 未运行"
    echo ""
    echo "在后台启动 Flask API..."
    python app.py &
    API_PID=$!
    echo "等待 API 启动..."
    sleep 3
    
    if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
        echo "✅ Flask API 启动成功"
        STARTED_API=true
    else
        echo "❌ 无法启动 Flask API"
        echo "请手动运行 run_flask.command"
        read -p "按 Enter 键退出..."
        exit 1
    fi
fi

echo ""
echo "🧪 运行测试套件..."
echo ""
echo "================================================"

# Run tests
python test_api.py

TEST_RESULT=$?

echo ""
echo "================================================"

# Stop API if we started it
if [ "$STARTED_API" = true ]; then
    echo ""
    echo "🛑 停止 Flask API..."
    kill $API_PID 2>/dev/null
fi

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ 所有测试完成"
else
    echo "⚠️  部分测试可能失败 - 请查看上面的输出"
fi

echo ""
read -p "按 Enter 键退出..."
