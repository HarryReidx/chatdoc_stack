from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import json
import time
import logging
import shutil
from enum import Enum
from typing import Optional, List, Dict, Any, Union
import asyncio
import httpx
from pathlib import Path

# 配置日志
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# 解析器类型枚举
class ParserType(str, Enum):
    MEGAPARSE = "megaparse"  # MegaParse解析器
    LLAMA_PARSE = "llamaparse"  # LlamaParse解析器
    QWEN = "qwen"  # 通义千问解析器
    MOCK = "mock"  # 模拟解析器

# 解析策略枚举
class ParseStrategy(str, Enum):
    AUTO = "auto"  # 自动选择最佳策略
    FAST = "fast"  # 快速解析
    HI_RES = "hi_res"  # 高精度解析

# 应用配置类
class AppConfig:
    """应用配置"""
    
    def __init__(self):
        # 解析器配置
        self.default_parser = ParserType(os.getenv("DEFAULT_PARSER", "megaparse"))
        self.megaparse_enabled = os.getenv("MEGAPARSE_ENABLED", "true").lower() == "true"
        self.llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY", "llx-your-api-key-here")
        self.qwen_api_key = os.getenv("QWEN_API_KEY", "your-qwen-api-key-here")
        
        # 服务配置
        self.port = int(os.getenv("PORT", "8080"))
        self.log_level = os.getenv("LOG_LEVEL", "info")
        self.temp_dir = os.getenv("TEMP_DIR", "./temp")
        
        # 创建临时目录
        os.makedirs(self.temp_dir, exist_ok=True)

# 创建配置实例
config = AppConfig()

# 创建FastAPI应用
app = FastAPI(
    title="多引擎文档解析服务",
    description="支持MegaParse、LlamaParse和通义千问的文档解析服务，替代TEXTIN PDF2MD API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 解析器基类
class BaseParser:
    """文档解析器基类"""
    
    def __init__(self):
        self.name = "base"
    
    async def parse(self, file_path: str, strategy: ParseStrategy = ParseStrategy.AUTO) -> str:
        """解析文档"""
        raise NotImplementedError("子类必须实现parse方法")

# MegaParse解析器
class MegaParseParser(BaseParser):
    """使用MegaParse解析文档"""
    
    def __init__(self):
        super().__init__()
        self.name = "megaparse"
        try:
            from megaparse import MegaParse
            from megaparse_sdk.schema.parser_config import StrategyEnum
            
            self.parser = MegaParse()
            self.strategy_map = {
                ParseStrategy.AUTO: StrategyEnum.AUTO,
                ParseStrategy.FAST: StrategyEnum.FAST,
                ParseStrategy.HI_RES: StrategyEnum.HI_RES
            }
            logger.info("MegaParse解析器初始化成功")
        except Exception as e:
            logger.error(f"MegaParse解析器初始化失败: {e}")
            raise
    
    async def parse(self, file_path: str, strategy: ParseStrategy = ParseStrategy.AUTO) -> str:
        """使用MegaParse解析文档"""
        try:
            from megaparse_sdk.schema.parser_config import StrategyEnum
            
            # 转换策略枚举
            mp_strategy = self.strategy_map.get(strategy, StrategyEnum.AUTO)
            
            # 异步解析文档
            result = await self.parser.aload(
                file_path=file_path,
                strategy=mp_strategy
            )
            
            # 如果结果不是字符串，转换为字符串
            if not isinstance(result, str):
                result = str(result)
                
            return result
        except Exception as e:
            logger.error(f"MegaParse解析失败: {e}")
            raise

# LlamaParse解析器
class LlamaParseParser(BaseParser):
    """使用LlamaParse解析文档"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.name = "llamaparse"
        self.api_key = api_key
        
        try:
            from llama_parse import LlamaParse
            
            self.parser = LlamaParse(
                api_key=api_key,
                result_type="markdown",
                verbose=True,
                language="zh",  # 支持中文
                parsing_instruction="请保持表格结构，提取所有文本内容"
            )
            logger.info("LlamaParse解析器初始化成功")
        except Exception as e:
            logger.error(f"LlamaParse解析器初始化失败: {e}")
            raise
    
    async def parse(self, file_path: str, strategy: ParseStrategy = ParseStrategy.AUTO) -> str:
        """使用LlamaParse解析文档"""
        try:
            # LlamaParse不支持策略选择，忽略strategy参数
            documents = self.parser.load_data(file_path)
            return documents[0].text if documents else ""
        except Exception as e:
            logger.error(f"LlamaParse解析失败: {e}")
            raise

# 通义千问解析器
class QwenParser(BaseParser):
    """使用通义千问API解析文档"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.name = "qwen"
        self.api_key = api_key
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.model = "qwen-plus"
        logger.info("通义千问解析器初始化成功")
    
    async def parse(self, file_path: str, strategy: ParseStrategy = ParseStrategy.AUTO) -> str:
        """使用通义千问API解析文档"""
        try:
            # 读取文件内容
            file_ext = Path(file_path).suffix.lower()
            
            # 对于PDF文件，使用PyMuPDF提取文本
            if file_ext == ".pdf":
                import fitz  # PyMuPDF
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
            # 对于Word文件，使用python-docx提取文本
            elif file_ext in [".docx", ".doc"]:
                from docx import Document
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
            # 对于文本文件，直接读取
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            
            # 如果文本太长，截断
            if len(text) > 10000:  # 通义千问API有输入长度限制
                text = text[:10000] + "\n...(内容已截断)"
            
            # 构造提示词
            prompt = f"""请将以下文档内容转换为Markdown格式，保留原文的结构和信息。特别注意：
1. 保持标题层级结构
2. 正确格式化表格
3. 保留列表和编号
4. 保持段落分隔

文档内容：
{text}
"""
            
            # 调用通义千问API
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "input": {
                            "messages": [
                                {"role": "system", "content": "你是一个专业的文档转换助手，擅长将文档转换为Markdown格式。"},
                                {"role": "user", "content": prompt}
                            ]
                        },
                        "parameters": {}
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"通义千问API调用失败: {response.text}")
                    raise HTTPException(status_code=500, detail=f"通义千问API调用失败: {response.status_code}")
                
                result = response.json()
                markdown_content = result.get("output", {}).get("text", "")
                return markdown_content
        except Exception as e:
            logger.error(f"通义千问解析失败: {e}")
            raise

class MockParser(BaseParser):
    """模拟解析器，用于演示和测试"""
    
    def __init__(self):
        super().__init__()
        self.name = "mock"
        logger.info("模拟解析器初始化成功")
    
    async def parse(self, file_path: str, strategy: ParseStrategy = ParseStrategy.AUTO) -> str:
        """模拟解析文档"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return f"# 解析错误\n\n文件不存在: {file_path}"
                
            # 获取文件扩展名
            file_ext = Path(file_path).suffix.lower()
            
            # 根据文件类型进行不同处理
            if file_ext == ".pdf":
                content = f"# 模拟PDF解析结果\n\n这是从 {file_path} 提取的模拟内容。\n\n"
                content += "## 第1页\n\n这是模拟的PDF内容第1页。\n\n"
                content += "## 第2页\n\n这是模拟的PDF内容第2页。\n\n"
                content += "### 2.1 小节\n\n这是一个模拟的小节内容。\n\n"
                content += "## 第3页\n\n这是模拟的PDF内容第3页，包含一个表格：\n\n"
                content += "| 列1 | 列2 | 列3 |\n| --- | --- | --- |\n| 数据1 | 数据2 | 数据3 |\n| 数据4 | 数据5 | 数据6 |\n\n"
            elif file_ext in [".docx", ".doc"]:
                content = f"# 模拟Word解析结果\n\n这是从 {file_path} 提取的模拟内容。\n\n"
                content += "## 第一章\n\n这是模拟的Word文档第一章内容。\n\n"
                content += "### 1.1 引言\n\n这是一个模拟的引言内容。\n\n"
                content += "## 第二章\n\n这是模拟的Word文档第二章内容。\n\n"
                content += "1. 第一点\n2. 第二点\n3. 第三点\n\n"
            elif file_ext in [".txt", ".md"]:
                # 对于文本文件，直接读取内容
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            else:
                content = f"# 未知文件类型\n\n无法解析文件类型: {file_ext}\n\n文件路径: {file_path}"
            
            return content
        except Exception as e:
            logger.error(f"模拟解析失败: {e}")
            return f"# 解析错误\n\n无法解析文件 {file_path}: {str(e)}"

# 解析器工厂类
class ParserFactory:
    """解析器工厂，用于创建和管理不同类型的解析器"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.parsers = {}
        self.default_parser_type = config.default_parser
        
    async def init_parsers(self):
        """初始化所有配置的解析器"""
        # 初始化MegaParse解析器
        try:
            if self.config.megaparse_enabled:
                self.parsers[ParserType.MEGAPARSE] = MegaParseParser()
                logger.info("MegaParse解析器已注册")
        except Exception as e:
            logger.error(f"MegaParse解析器初始化失败: {e}")
        
        # 初始化LlamaParse解析器
        try:
            if self.config.llama_cloud_api_key and self.config.llama_cloud_api_key != "llx-your-api-key-here":
                self.parsers[ParserType.LLAMAPARSE] = LlamaParseParser(self.config.llama_cloud_api_key)
                logger.info("LlamaParse解析器已注册")
        except Exception as e:
            logger.error(f"LlamaParse解析器初始化失败: {e}")
        
        # 初始化通义千问解析器
        try:
            if self.config.qwen_api_key and self.config.qwen_api_key != "your-qwen-api-key-here":
                self.parsers[ParserType.QWEN] = QwenParser(self.config.qwen_api_key)
                logger.info("通义千问解析器已注册")
        except Exception as e:
            logger.error(f"通义千问解析器初始化失败: {e}")
        
        # 始终初始化模拟解析器作为后备
        self.parsers[ParserType.MOCK] = MockParser()
        
        # 如果没有可用的解析器，使用模拟解析器作为默认
        if not self.parsers or self.default_parser_type not in self.parsers:
            self.default_parser_type = ParserType.MOCK
            logger.warning(f"没有可用的解析器，将使用模拟解析器作为默认")
    
    def get_parser(self, parser_type: ParserType = None) -> BaseParser:
        """获取指定类型的解析器"""
        if parser_type is None:
            parser_type = self.default_parser_type
        
        # 如果请求的解析器不可用，使用默认解析器
        if parser_type not in self.parsers:
            logger.warning(f"请求的解析器类型 {parser_type} 不可用，将使用默认解析器 {self.default_parser_type}")
            parser_type = self.default_parser_type
        
        return self.parsers[parser_type]

# 全局变量存储解析器工厂实例
parser_factory = None

async def init_parser():
    """初始化解析器工厂"""
    global parser_factory
    parser_factory = ParserFactory(config)
    await parser_factory.init_parsers()

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化解析器工厂"""
    await init_parser()

@app.post("/api/v1/pdf_to_markdown")
async def pdf_to_markdown(
    request: Request,
    file: Optional[UploadFile] = File(None),
    parser_type: ParserType = Query(None, description="解析器类型，支持megaparse、llamaparse、qwen和mock"),
    strategy: ParseStrategy = Query(ParseStrategy.AUTO, description="解析策略，支持auto、fast和hi_res"),
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
    兼容原有的参数格式，同时支持多种解析引擎和策略
    支持两种方式上传文件：
    1. 通过multipart/form-data上传文件（FastAPI标准方式）
    2. 直接将文件内容作为请求体（兼容TextIn API方式）
    """
    start_time = time.time()
    
    # 确定文件内容和文件名
    if file:
        # 方式1：通过multipart/form-data上传的文件
        filename = file.filename
        file_size = 0  # 将在读取内容后更新
        content = await file.read()
        file_size = len(content)
    else:
        # 方式2：直接将文件内容作为请求体
        content = await request.body()
        if not content:
            raise HTTPException(status_code=400, detail="请求体为空")
        
        # 从请求头或查询参数中获取文件名
        filename = request.headers.get("x-file-name", "document.pdf")
        file_size = len(content)
    
    # 从文件名确定文件类型
    file_ext = filename.lower().split('.')[-1] if '.' in filename else "pdf"
    if file_ext not in ['pdf', 'docx', 'doc', 'txt', 'md']:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file_ext}")
    
    logger.info(f"开始解析文件: {filename}, 大小: {file_size} bytes, 解析器: {parser_type}, 策略: {strategy}")
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
        try:
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
            
            logger.info(f"临时文件保存至: {tmp_file_path}")
            
            # 获取指定类型的解析器
            parser = parser_factory.get_parser(parser_type)
            logger.info(f"使用 {parser.name} 解析器处理文件")
            
            # 使用解析器解析文档
            markdown_content = await parser.parse(tmp_file_path, strategy)
            
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
                    "engine": parser.name,
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
                    "filename": filename,
                    "size": file_size,
                    "type": file_ext
                },
                "parser": parser.name,
                "strategy": strategy.value
            }
            
            logger.info(f"文件解析完成: {filename}, 耗时: {process_time:.2f}s, 页数: {estimated_pages}")
            
            return result
            
        except Exception as e:
            logger.error(f"文件解析失败: {filename}, 错误: {str(e)}")
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
        "available_parsers": [p.name for p in parser_factory.parsers.values()],
        "default_parser": parser_factory.default_parser_type.value,
        "timestamp": time.time()
    }

@app.get("/api/v1/parsers")
async def list_parsers():
    """列出所有可用的解析器"""
    return {
        "parsers": [{
            "name": parser.name,
            "type": parser_type.value
        } for parser_type, parser in parser_factory.parsers.items()],
        "default": parser_factory.default_parser_type.value
    }

@app.get("/")
async def root():
    """根路径，返回服务信息"""
    return {
        "message": "多引擎文档解析服务", 
        "docs_url": "/docs",
        "available_parsers": [p.name for p in parser_factory.parsers.values()],
        "default_parser": parser_factory.default_parser_type.value,
        "version": "1.0.0"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"全局异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"服务器内部错误: {str(exc)}",
            "type": type(exc).__name__
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
