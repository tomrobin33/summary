import sys
import socket
import subprocess
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return PlainTextResponse("Stdio server is running.")

if __name__ == "__main__":
    # 检查 8080 端口是否被占用
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("0.0.0.0", 8080))
    sock.close()
    if result == 0:
        print("[WARN] 端口 8080 已被占用，尝试自动关闭占用进程...", file=sys.stderr)
        try:
            # lsof 查找占用端口的进程
            output = subprocess.check_output(["lsof", "-i:8080", "-t"])
            pids = output.decode().strip().split("\n")
            for pid in pids:
                if pid:
                    print(f"[INFO] 杀掉进程 PID: {pid}", file=sys.stderr)
                    subprocess.run(["kill", "-9", pid])
            print("[INFO] 已关闭占用 8080 的进程，继续启动服务。", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] 自动关闭进程失败: {e}", file=sys.stderr)
            sys.exit(1)
    # 监听所有地址，端口为 8080
    uvicorn.run("mcp_server.stdio_server:app", host="0.0.0.0", port=8080, reload=False) 