import sys
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return PlainTextResponse("Stdio server is running.")

if __name__ == "__main__":
    # 监听所有地址，端口改为 18080，避免云端端口冲突
    uvicorn.run("mcp_server.stdio_server:app", host="0.0.0.0", port=18080, reload=False) 