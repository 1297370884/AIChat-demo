# AI Chat Application

基于Vue3前端 + Robyn异步框架后端的智能聊天应用，支持流式内容生成与Markdown渲染

## 技术栈
- **前端**: Vue3 + TypeScript + Element Plus + Markdown-it
- **后端**: Python Robyn框架 + OpenAI API兼容接口
- **特性**: 异步处理/流式响应/打字机效果/模型配置化

## 核心功能
✅ 实时流式内容生成与逐字渲染  
✅ Markdown语法高亮与格式渲染  
✅ 模型参数动态配置：
   - 修改`server/model.py`中的：
   ```python
   MODEL_NAME = "gpt-3.5-turbo"  # 模型标识
   API_KEY = "sk-your-key"      # 服务商API密钥
   BASE_URL = "https://api.openai.com/v1"  # 模型服务地址
   ```
✅ 对话历史持久化存储  
✅ 响应延迟实时监测

## 快速开始
1. 启动后端：
   ```bash
   cd server
   pip install -r requirements.txt
   python app.py
   ```
2. 启动前端：
   ```bash
   cd client
   npm install
   npm run dev
   ```
## 注意
- 后端模型需要使用OpenAI API兼容接口，请自行替换为实际的API密钥和地址
- 使用前关闭代理
- 使用前请先启动后端
- 刷新前端页面可开启新的聊天会话
- demo版本暂未开发其他功能...

