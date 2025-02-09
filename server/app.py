from robyn import Robyn, WebSocket
import asyncio
from model import AiChat
import uuid
import json
import time

app = Robyn(__file__)
websocket = WebSocket(app, "/ws")

active_ws = {}  # 保存 WebSocket 实例和对应的状态
HEARTBEAT_INTERVAL = 30  # 心跳间隔30秒
HEARTBEAT_TIMEOUT = 60   # 超时时间60秒

async def heartbeat_checker():
    """心跳检测后台任务"""
    while True:
        now = time.time()
        to_remove = []
        
        for ws_id, data in active_ws.items():
            # 检查心跳超时
            if now - data["last_activity"] > HEARTBEAT_TIMEOUT:
                print(f"连接 {ws_id} 心跳超时，关闭连接")
                to_remove.append(ws_id)
                await data["ws"].async_close()
                
            # 发送心跳ping
            elif now - data["last_ping"] > HEARTBEAT_INTERVAL:
                try:
                    # 确保心跳包包含所有必要字段
                    await data["ws"].async_send_to(ws_id, json.dumps({
                        "type": "heartbeat_ping",
                        "timestamp": now,
                        "message": "ping"  # 添加验证字段
                    }))
                    data["last_ping"] = now
                    data["waiting_pong"] = True
                except Exception as e:
                    print(f"发送心跳失败: {str(e)}")
                    to_remove.append(ws_id)
        
        # 清理失效连接
        for ws_id in to_remove:
            del active_ws[ws_id]
        
        await asyncio.sleep(5)  # 每5秒检查一次

@websocket.on("connect")
async def handle_connect(ws):
    print(f"客户端 {ws.id} 已连接")
    active_ws[ws.id] = {
        "ai_chat": AiChat(),
        "current_stream_id": None,
        "last_activity": time.time(),  # 最后活动时间
        "last_ping": time.time(),       # 最后发送ping时间
        "waiting_pong": False,          # 是否在等待pong响应
        "ws": ws                        # 保存ws实例
    }
    await ws.async_send_to(ws.id, json.dumps({
        "type": "system",
        "content": f"欢迎{ws.id}来到AI聊天室！"
    }))
    return ""

@websocket.on("close")
async def handle_close(ws):
    if ws.id in active_ws:
        try:
            await active_ws[ws.id]["ws"].async_close()
        except Exception as e:
            print(f"关闭连接时出错: {str(e)}")
        finally:
            del active_ws[ws.id]
    return ""

@websocket.on("message")
async def handle_message(ws, msg):
    try:
        # 增加空消息检查
        if not msg or msg.strip() == "":
            return ""

        data = active_ws.get(ws.id)
        if not data:
            return ""

        # 更新最后活动时间
        data["last_activity"] = time.time()
        
        # 解析JSON消息
        try:
            msg_data = json.loads(msg)
        except json.JSONDecodeError:
            await ws.async_send_to(ws.id, json.dumps({
                "type": "error",
                "content": "消息格式错误，请使用JSON格式"
            }))
            return ""

        # 优先处理心跳响应
        if msg_data.get("type") == "heartbeat_pong":
            data["waiting_pong"] = False
            return ""

        # 过滤非用户消息
        if msg_data.get("type") != "user":
            print(f"收到非用户消息类型: {msg_data.get('type')}")
            return ""

        # 加强内容验证
        content = msg_data.get("content", "").strip()
        if not content:
            await ws.async_send_to(ws.id, json.dumps({
                "type": "error",
                "content": "消息内容不能为空"
            }))
            return ""

        # 处理普通消息（保持原有逻辑）
        print(f"[用户{ws.id}] {msg_data.get('content', '')}")
        
        stream_id = str(uuid.uuid4())
        active_ws[ws.id]["current_stream_id"] = stream_id

        await ws.async_send_to(ws.id, json.dumps({
            "type": "stream_start",
            "stream_id": stream_id
        }))

        async for ai_response in data["ai_chat"].chat(content=content):
            # 增加响应内容检查
            if ai_response is None:
                continue
            await ws.async_send_to(ws.id, json.dumps({
                "type": "stream_chunk",
                "stream_id": stream_id,
                "content": ai_response or ""  # 确保不为None
            }))

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
    return ""

# 添加启动事件
@app.startup_handler
async def startup_handler():
    asyncio.create_task(heartbeat_checker())
    print("WebSocket服务已启动，心跳检测已启用")

if __name__ == "__main__":
    app.start(port=8000, host="0.0.0.0")