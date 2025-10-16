# 📊 Company Information API - 使用指南

> 快速入门：获取公司信息的 API 和可视化界面

## 🚀 快速开始（推荐方式）

### 方法一：双击运行（macOS 用户）

1. **首次使用** - 双击 `setup.command` 安装环境
2. **启动界面** - 双击 `run_streamlit.command` 
3. **浏览器自动打开** → http://localhost:8501

### 方法二：命令行（所有平台）

```bash
# 创建环境（首次）
conda create -n projAPI python=3.12
conda activate projAPI

# 安装依赖
pip install -r requirements_streamlit.txt

# 运行 Streamlit 界面
streamlit run streamlit_app.py

# 或运行 Flask API
python app.py
```

## 💡 三种使用方式

### 1️⃣ Streamlit 网页界面（推荐新手）
- 📊 可视化仪表板
- 🖱️ 点击按钮即可查询
- 📥 支持导出 JSON 数据
- 🔌 内置 API 使用教程

**访问地址：** http://localhost:8501

### 2️⃣ Flask REST API（推荐开发者）
- 🚀 RESTful API 接口
- 📡 返回 JSON 格式数据
- 🔧 方便程序集成

**访问地址：** http://localhost:5001

**示例调用：**
```bash
# 查询苹果公司信息
curl http://localhost:5001/api/company/AAPL

# Python 调用
import requests
data = requests.get('http://localhost:5001/api/company/AAPL').json()
```

### 3️⃣ 同时运行两个服务

在两个终端分别运行：
```bash
# 终端 1：Flask API
python app.py

# 终端 2：Streamlit 界面
streamlit run streamlit_app.py
```

## 📋 常用命令

```bash
# 激活环境
conda activate projAPI

# 运行 Streamlit
streamlit run streamlit_app.py

# 运行 Flask API
python app.py

# 运行测试
python test_api.py

# 停止服务器
按 Ctrl+C
```

## 🎯 热门股票代码

| 公司 | 代码 | 公司 | 代码 |
|------|------|------|------|
| 苹果 | AAPL | 微软 | MSFT |
| 谷歌 | GOOGL | 亚马逊 | AMZN |
| 特斯拉 | TSLA | Meta | META |
| 英伟达 | NVDA | 网飞 | NFLX |

## 🔧 常见问题

**Q: 提示模块未找到？**
```bash
conda activate projAPI
pip install -r requirements_streamlit.txt
```

**Q: 端口被占用？**
```bash
# Streamlit 换端口
streamlit run streamlit_app.py --server.port 8502
```

**Q: conda 未找到？**  
需要先安装 Anaconda 或 Miniconda

**Q: 双击 .command 文件没反应？**
```bash
# 添加执行权限
chmod +x *.command
```

## 📚 更多文档

- **README.md** - 完整英文文档
- **QUICKSTART.md** - 快速入门（英文）
- **COMMANDS.md** - 命令参考

## 🎓 学习路径

**完全新手：**
1. 双击 `setup.command` 安装
2. 双击 `run_streamlit.command` 启动
3. 在网页界面探索各个标签页
4. 尝试点击热门股票按钮

**开发者：**
1. 运行 Flask API：`python app.py`
2. 用 curl 测试：`curl http://localhost:5001/api/company/AAPL`
3. 查看 Streamlit 的 "API Usage" 标签页
4. 集成到自己的项目

**高级用户：**
1. 同时运行 Flask + Streamlit
2. 修改代码添加新功能
3. 运行测试：`python test_api.py`
4. 部署到云端（见 README.md）

## 💻 技术栈

- **Python 3.12** - 编程语言
- **Flask 3.0.0** - API 框架
- **Streamlit 1.40+** - 界面框架
- **yfinance 0.2.32** - 数据源
- **Pandas** - 数据处理

## 📁 项目文件

```
project/
├── app.py                    # Flask API 服务器
├── streamlit_app.py          # Streamlit 界面
├── test_api.py               # 测试脚本
│
├── setup.command             # 安装脚本（双击）
├── run_streamlit.command     # 启动界面（双击）
├── run_flask.command         # 启动 API（双击）
├── run_tests.command         # 运行测试（双击）
│
├── requirements.txt          # Flask 依赖
├── requirements_streamlit.txt # 完整依赖
│
└── 文档/
    ├── README.md             # 主文档（英文）
    ├── QUICKSTART.md         # 快速入门（英文）
    ├── COMMANDS.md           # 命令参考
    └── 使用指南.md          # 本文件（中文）
```

## 🎉 就这么简单！

选择适合你的方式开始使用：
- 🖱️ **最简单** → 双击 `.command` 文件
- ⌨️ **通用** → 使用命令行
- 🔌 **开发** → 直接调用 API

---

**有问题？** 查看 README.md 或运行 `python test_api.py` 测试功能
