from robyn import Robyn, WebSocket
import asyncio
from model import AiChat
import uuid
import json

app = Robyn(__file__)
websocket = WebSocket(app, "/ws")

active_ws = {}  # 保存 WebSocket 实例和对应的 AiChat 对象

@websocket.on("connect")
async def handle_connect(ws):
    print(f"客户端 {ws.id} 已连接")
    ai_chat = AiChat()  # 创建 AiChat 实例
    active_ws[ws.id] = {
        "ai_chat": ai_chat,
        "current_stream_id": None  # 当前流ID
    }  # 将 AiChat 绑定到 WebSocket 连接
    await ws.async_send_to(ws.id, json.dumps({
        "type": "system",
        "content": f"欢迎{ws.id}来到AI聊天室！"
    }))
    return ""


@websocket.on("close")
async def handle_close(ws):
    if ws.id in active_ws:
        del active_ws[ws.id]
    return f"连接断开/n客户端 {ws.id} 已断开"


@websocket.on("message")
async def handle_message(ws, msg):
    try:
        print(f"[用户{ws.id}] {msg}")
        data = active_ws.get(ws.id) # 获取对应的 data实例
        if not data:
            return 
        
         # 生成唯一流ID
        stream_id = str(uuid.uuid4())
        active_ws[ws.id]["current_stream_id"] = stream_id


        # 发送流开始标记
        await ws.async_send_to(ws.id, json.dumps({
            "type": "stream_start",
            "stream_id": stream_id
        }))

        # 调用 AI 接口并处理流式响应
        async for ai_response in data["ai_chat"].chat(content=msg):
            await ws.async_send_to(ws.id, json.dumps({
                "type": "stream_chunk",
                "stream_id": stream_id,
                "content": ai_response
            }))

        # 发送流结束标记
        await ws.async_send_to(ws.id, json.dumps({
            "type": "stream_end",
            "stream_id": stream_id
        }))

    except Exception as e:
        error_msg = f"系统错误：{str(e)}"
        await ws.async_send_to(ws.id, json.dumps({
            "type": "error",
            "content": error_msg
        }))
    return "消息发送成功"


if __name__ == "__main__":
    app.start(port=8000, host="0.0.0.0")