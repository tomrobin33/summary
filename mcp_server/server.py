from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from mcp_server.utils import download_file, detect_file_type
from mcp_server.parser_excel import parse_excel
from mcp_server.parser_word import parse_word
from mcp_server.parser_ppt import parse_ppt
from mcp_server.exceptions import FileDownloadError, FileTypeError
import os

app = FastAPI()

class ParseRequest(BaseModel):
    url: str
    file_type: Optional[str] = None

@app.post("/parse_file")
def parse_file(req: ParseRequest):
    try:
        tmp_path, file_type = download_file(req.url, req.file_type)
    except FileDownloadError as e:
        return {"error": str(e)}
    except FileTypeError as e:
        return {"error": str(e)}
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
    return {"file_type": file_type, "content": content} 