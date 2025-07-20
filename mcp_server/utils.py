import tempfile
import requests
from mcp_server.exceptions import FileDownloadError, FileTypeError

def detect_file_type(url, file_type=None):
    if file_type:
        return file_type
    if url.endswith('.xlsx'):
        return 'excel'
    elif url.endswith('.docx'):
        return 'word'
    elif url.endswith('.pptx'):
        return 'ppt'
    else:
        raise FileTypeError('无法识别文件类型')

def download_file(url, file_type=None):
    response = requests.get(url)
    if response.status_code != 200:
        raise FileDownloadError('下载失败')
    file_type = detect_file_type(url, file_type)
    suffix = {
        'excel': '.xlsx',
        'word': '.docx',
        'ppt': '.pptx'
    }.get(file_type, '')
    if not suffix:
        raise FileTypeError('不支持的文件类型')
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name
    return tmp_path, file_type 