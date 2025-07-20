# MCP 文件解析服务器

## 项目简介
本项目为多格式文件解析 MCP 服务器，支持通过 URL 接收并解析 Excel、Word、PPT 文件，自动提取内容并返回结构化 JSON，便于大模型理解和处理。

## 主要功能
- 支持通过 URL 上传 Excel、Word、PPT 文件
- 自动识别文件类型并解析内容
- 统一输出结构化 JSON
- 便于扩展更多文件类型

## 目录结构
- mcp_server/ 业务代码
  - server.py FastAPI 启动与路由
  - parser_excel.py Excel 解析
  - parser_word.py Word 解析
  - parser_ppt.py PPT 解析
  - exceptions.py 自定义异常
  - utils.py 工具函数
- assets/ 静态资源
- docs/ 项目文档
- tests/ 单元测试

## 接口说明
### POST /parse_file
- 参数：
  - url: 文件下载链接
  - file_type: 文件类型（可选，excel/word/ppt，自动识别）
- 返回：
  - file_type: 文件类型
  - content: 结构化内容 JSON

## 依赖安装
```bash
pip install -r requirements.txt
```

## 启动方法
```bash
uvicorn mcp_server.server:app --reload
```

## 开发规范
- 业务逻辑拆分为独立模块，便于维护和扩展
- 所有异常集中处理，保证接口健壮性
- 推荐使用 Python 3.12 及以上版本
- 单元测试覆盖主要接口 