# AI Chat Application

基于Vue3前端 + Robyn异步框架后端的websocket智能聊天应用，支持流式内容生成与Markdown渲染

## 技术栈
- **前端**: Vue3 + TypeScript + Element Plus + Markdown-it
- **后端**: Python Robyn框架 + OpenAI API兼容接口
- **特性**: 异步处理/流式响应/打字机效果/模型配置化/websocket心跳检测与自动重连

## 核心功能
✅ 实时流式内容生成与逐字渲染
✅ websocket心跳检测与自动重连
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

## 数据格式
### 前端发送的数据格式
```json
{
  "type": "user",
  "content": "你好",
  "timestamp": 1739095604951
}
```

### 前端接收到的数据格式
#### 系统消息
```json
{
  "type": "system",
  "content": "欢迎16b7fe45-e4b9-48fb-b72c-a134733c0b6f来到AI聊天室！"
}
```

#### ai回复流式消息
```json
{
  "type": "stream_start",
  "stream_id": "efcd4609-9e70-44f3-92bb-2950ecf62292"
}

{
  "type": "stream_chunk",
  "stream_id": "efcd4609-9e70-44f3-92bb-2950ecf62292",
  "content": "你好"
}

{
  "type": "stream_chunk",
  "stream_id": "efcd4609-9e70-44f3-92bb-2950ecf62292",
  "content": "有什么"
}

{
  "type": "stream_chunk",
  "stream_id": "efcd4609-9e70-44f3-92bb-2950ecf62292",
  "content": "可以帮助"
}

{
  "type": "stream_end",
  "stream_id": "efcd4609-9e70-44f3-92bb-2950ecf62292"
}
```

#### 错误消息
```json
{
  "type": "error",
  "content": "系统错误：Connection error."
}
```

#### 心跳检测数据格式
后端发送心跳检测
```json
{
  "type": "heartbeat_ping",
  "timestamp": 1739094952.1532173,
  "message": "ping"
}
```
前端发送心跳响应
```json
{
  "type": "heartbeat_pong",
  "timestamp": 1739095633.311393
}
```

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

