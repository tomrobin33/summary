from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from mcp_server.utils import download_file, detect_file_type
from mcp_server.parser_excel import parse_excel
from mcp_server.parser_word import parse_word
from mcp_server.parser_ppt import parse_ppt
from mcp_server.exceptions import FileDownloadError, FileTypeError
import os
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

class ParseRequest(BaseModel):
    url: str
    file_type: Optional[str] = None

@app.post("/parse_file")
def parse_file(req: ParseRequest):
    def event_stream():
        try:
            yield f"data: {json.dumps({'status': 'downloading'})}\n\n"
            tmp_path, file_type = download_file(req.url, req.file_type)
        except FileDownloadError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            return
        except FileTypeError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            return
        yield f"data: {json.dumps({'status': 'parsing', 'file_type': file_type})}\n\n"
        try:
            if file_type == 'excel':
                content = parse_excel(tmp_path)
            elif file_type == 'word':
                content = parse_word(tmp_path)
            elif file_type == 'ppt':
                content = parse_ppt(tmp_path)
            else:
                content = []
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        yield f"data: {json.dumps({'file_type': file_type, 'content': content})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream") 