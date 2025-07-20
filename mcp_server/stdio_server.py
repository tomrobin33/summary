import sys
import socket
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
from fastapi.responses import StreamingResponse
import json
import time

app = FastAPI()

@app.get("/")
def read_root():
    def event_stream():
        try:
            yield f"data: {{\"status\": \"ready\"}}\n\n"
            while True:
                yield f"data: {{\"heartbeat\": \"alive\"}}\n\n"
                time.sleep(5)
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/sse")
def sse():
    def event_stream():
        try:
            yield f"data: {{\"status\": \"ready\"}}\n\n"
            while True:
                yield f"data: {{\"heartbeat\": \"alive\"}}\n\n"
                time.sleep(5)
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    # 检查 8080 端口是否被占用
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("0.0.0.0", 8080))
    sock.close()
    if result == 0:
        print("[ERROR] 端口 8080 已被占用，服务未启动。请检查是否有其他进程或平台多实例占用该端口。", file=sys.stderr)
        sys.exit(1)
    # 监听所有地址，端口为 8080
    uvicorn.run("mcp_server.stdio_server:app", host="0.0.0.0", port=8080, reload=False) 