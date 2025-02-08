from robyn import Robyn, WebSocket
import random
import asyncio
from model_stream import AiChat

app = Robyn(__file__)
websocket = WebSocket(app, "/ws")

active_ws = {}  # 保存 WebSocket 实例和对应的 AiChat 对象

@websocket.on("connect")
async def handle_connect(ws):
    print(f"客户端 {ws.id} 已连接")
    ai_chat = AiChat()  # 创建 AiChat 实例
    active_ws[ws.id] = ai_chat  # 将 AiChat 绑定到 WebSocket 连接
    await ws.async_send_to(ws.id, "系统：欢迎来到AI聊天室！")
    return "连接成功"


@websocket.on("close")
async def handle_close(ws):
    if ws.id in active_ws:
        del active_ws[ws.id]
    print(f"客户端 {ws.id} 已断开")
    return "连接断开"


@websocket.on("message")
async def handle_message(ws, msg):  # 修改为接收bytes类型
    try:
        print(f"[用户{ws.id}] {msg}")
        ai_chat = active_ws.get(ws.id)  # 获取对应的 AiChat 实例

        # 发送思考中状态
        await ws.async_send_to(ws.id, "系统：AI正在思考...")

        # 调用 AI 接口并处理流式响应
        async for ai_response in ai_chat.chat(content=msg):
            # 实时发送流式内容
            await ws.async_send_to(ws.id, f"AI：{ai_response}")

    except Exception as e:
        error_msg = f"系统错误：{str(e)}"
        await ws.async_send_to(ws.id, error_msg)
    return "消息发送成功"


if __name__ == "__main__":
    app.start(port=8000, host="0.0.0.0")