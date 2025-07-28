from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import tempfile
import os
import json
import time
import logging
from typing import Optional
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Custom Document Parser",
    description="替代 TEXTIN API 的文档解析服务",
    version="1.0.0"
)

# 全局变量存储解析器实例
parser = None

async def init_parser():
    """初始化 LlamaParse"""
    global parser
    try:
        from llama_parse import LlamaParse
        
        # 从环境变量获取 API Key
        api_key = os.getenv("LLAMA_CLOUD_API_KEY", "llx-your-api-key-here")
        
        if api_key == "llx-your-api-key-here":
            logger.warning("请设置 LLAMA_CLOUD_API_KEY 环境变量")
            # 为了演示，我们创建一个模拟解析器
            parser = MockParser()
        else:
            parser = LlamaParse(
                api_key=api_key,
                result_type="markdown",
                verbose=True,
                language="zh",  # 支持中文
                parsing_instruction="请保持表格结构，提取所有文本内容"
            )
        
        logger.info("文档解析器初始化成功")
    except Exception as e:
        logger.error(f"解析器初始化失败: {e}")
        # 使用模拟解析器作为后备
        parser = MockParser()

class MockParser:
    """模拟解析器，用于演示和测试"""
    
    def load_data(self, file_path: str):
        """模拟文档解析"""
        logger.info(f"模拟解析文件: {file_path}")
        
        # 模拟解析延迟
        time.sleep(2)
        
        # 返回模拟的解析结果
        class MockDocument:
            def __init__(self):
                self.text = """# 文档标题

这是一个模拟解析的文档内容。

## 章节1
这里是第一章节的内容。

### 表格示例
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |

## 章节2
这里是第二章节的内容，包含更多详细信息。

**注意**: 这是模拟解析结果，请配置真实的 LLAMA_CLOUD_API_KEY 以获得实际解析功能。
"""
        
        return [MockDocument()]

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化解析器"""
    await init_parser()

@app.post("/api/v1/pdf_to_markdown")
async def pdf_to_markdown(
    file: UploadFile = File(...),
    dpi: Optional[int] = 144,
    page_start: Optional[int] = 0,
    page_count: Optional[int] = 2000,
    apply_document_tree: Optional[int] = 1,
    markdown_details: Optional[int] = 1,
    page_details: Optional[int] = 1,
    table_flavor: Optional[str] = "html",
    get_image: Optional[str] = "page",
    parse_mode: Optional[str] = "auto",
    char_details: Optional[int] = 1
):
    """
    替代 TEXTIN PDF2MD API
    兼容原有的参数格式
    """
    start_time = time.time()
    
    # 验证文件类型
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    file_ext = file.filename.lower().split('.')[-1]
    if file_ext not in ['pdf', 'docx', 'doc', 'txt']:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}")
    
    logger.info(f"开始解析文件: {file.filename}, 大小: {file.size} bytes")
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
        try:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
            
            logger.info(f"临时文件保存至: {tmp_file_path}")
            
            # 使用解析器解析文档
            documents = parser.load_data(tmp_file_path)
            
            # 提取解析结果
            markdown_content = documents[0].text if documents else ""
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 模拟页面信息（简化版本）
            estimated_pages = max(1, len(markdown_content) // 2000)  # 估算页数
            
            # 构造兼容 TEXTIN API 的返回格式
            result = {
                "code": 200,
                "result": {
                    "detail": markdown_content,
                    "pages": [
                        {
                            "num": i,
                            "content": [],
                            "structured": []
                        } for i in range(estimated_pages)
                    ],
                    "engine": "llamaparse",
                    "version": "1.0.0"
                },
                "metrics": [
                    {
                        "image_id": None,
                        "page_num": i
                    } for i in range(estimated_pages)
                ],
                "processing_time": round(process_time, 2),
                "file_info": {
                    "filename": file.filename,
                    "size": file.size,
                    "type": file_ext
                }
            }
            
            logger.info(f"文件解析完成: {file.filename}, 耗时: {process_time:.2f}s, 页数: {estimated_pages}")
            
            return result
            
        except Exception as e:
            logger.error(f"文件解析失败: {file.filename}, 错误: {str(e)}")
            raise HTTPException(status_code=500, detail=f"文档解析失败: {str(e)}")
        
        finally:
            # 清理临时文件
            try:
                os.unlink(tmp_file_path)
                logger.info(f"临时文件已清理: {tmp_file_path}")
            except Exception as e:
                logger.warning(f"临时文件清理失败: {e}")

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "custom-document-parser",
        "version": "1.0.0",
        "parser_ready": parser is not None,
        "timestamp": time.time()
    }

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Custom Document Parser Service",
        "version": "1.0.0",
        "endpoints": {
            "parse": "/api/v1/pdf_to_markdown",
            "health": "/health"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"未处理的异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务内部错误",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
