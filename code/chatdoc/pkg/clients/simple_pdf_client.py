"""
简单PDF客户端 - 兼容性替代方案
Author: AI Assistant
Date: 2025-07-28
"""
import json
import tempfile
import os
from typing import Dict, Any
from pkg.utils.logger import logger


class SimplePDFClient:
    """简单PDF客户端 - 使用PyPDF2"""
    
    def __init__(self):
        self.has_pypdf2 = False
        try:
            import PyPDF2
            self.has_pypdf2 = True
            logger.info("SimplePDFClient: 使用PyPDF2解析PDF")
        except ImportError:
            logger.warning("SimplePDFClient: PyPDF2未安装，使用备选方案")
    
    def recognize_pdf2md(self, image: bytes) -> 'MockResponse':
        """
        PDF转Markdown解析
        :param image: PDF文件的字节数据
        :return: 兼容TEXTIN格式的响应对象
        """
        try:
            if self.has_pypdf2:
                return self._parse_with_pypdf2(image)
            else:
                return self._parse_fallback(image)
                
        except Exception as e:
            logger.error(f"SimplePDFClient解析失败: {str(e)}")
            return self._parse_error(str(e))
    
    def _parse_with_pypdf2(self, pdf_bytes: bytes) -> 'MockResponse':
        """使用PyPDF2解析PDF"""
        import PyPDF2
        import io
        
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            pages = []
            full_text = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                
                # 简单的Markdown格式化
                markdown_text = f"# 第{page_num + 1}页\n\n{page_text}"
                
                pages.append({
                    "page_index": page_num,
                    "markdown": markdown_text,
                    "elements": self._extract_elements(page_text, page_num),
                    "images": []
                })
                
                full_text += markdown_text + "\n\n"
            
            # 构造兼容TEXTIN的响应格式
            result = {
                "code": 200,
                "message": "success",
                "result": {
                    "pages": pages,
                    "markdown": full_text,
                    "document_tree": self._build_document_tree(full_text),
                },
                "metrics": [{"page_index": i, "confidence": 0.85} for i in range(len(pages))]
            }
            
            logger.info(f"SimplePDFClient: 成功解析PDF，页数: {len(pages)}")
            return MockResponse(result)
            
        except Exception as e:
            logger.error(f"PyPDF2解析失败: {str(e)}")
            return self._parse_error(str(e))
    
    def _parse_fallback(self, pdf_bytes: bytes) -> 'MockResponse':
        """备选解析方案"""
        result = {
            "code": 200,
            "message": "success",
            "result": {
                "pages": [{
                    "page_index": 0,
                    "markdown": "# 文档内容\n\n无法解析PDF内容，请安装PyPDF2进行PDF解析。\n\n文档大小: {} bytes".format(len(pdf_bytes)),
                    "elements": [{
                        "line_index": 0,
                        "content": "无法解析PDF内容",
                        "type": "paragraph",
                        "bbox": [0, 0, 500, 20, 500, 20, 0, 20]
                    }],
                    "images": []
                }],
                "markdown": "# 文档内容\n\n无法解析PDF内容，请安装PyPDF2进行PDF解析。",
                "document_tree": {"title": "Document", "level": 0, "children": []},
            },
            "metrics": [{"page_index": 0, "confidence": 0.5}]
        }
        
        logger.warning("SimplePDFClient: 使用备选方案，无法解析PDF内容")
        return MockResponse(result)
    
    def _parse_error(self, error_msg: str) -> 'MockResponse':
        """错误处理"""
        result = {
            "code": 500,
            "message": f"PDF解析失败: {error_msg}",
            "result": {
                "pages": [{
                    "page_index": 0,
                    "markdown": f"# 解析错误\n\n{error_msg}",
                    "elements": [],
                    "images": []
                }],
                "markdown": f"# 解析错误\n\n{error_msg}",
                "document_tree": {"title": "Error", "level": 0, "children": []},
            },
            "metrics": [{"page_index": 0, "confidence": 0.0}]
        }
        
        return MockResponse(result)
    
    def _extract_elements(self, text: str, page_num: int) -> list:
        """从文本中提取元素信息"""
        elements = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            element = {
                "line_index": i,
                "content": line,
                "bbox": [0, i*20, 500, (i+1)*20, 500, (i+1)*20, 0, (i+1)*20],
                "page_index": page_num
            }
            
            # 简单的元素类型判断
            if len(line) < 50 and not line.endswith('。'):
                element["type"] = "title"
            else:
                element["type"] = "paragraph"
            
            elements.append(element)
        
        return elements
    
    def _build_document_tree(self, markdown_content: str) -> Dict[str, Any]:
        """构建文档树结构"""
        lines = markdown_content.split('\n')
        tree = {
            "title": "Document",
            "level": 0,
            "children": []
        }
        
        current_chapter = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                chapter = {
                    "title": title,
                    "level": 1,
                    "children": []
                }
                tree["children"].append(chapter)
                current_chapter = chapter
        
        return tree


class MockResponse:
    """模拟requests.Response对象，兼容原有代码"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.status_code = 200 if data.get("code") == 200 else 500
    
    def raise_for_status(self):
        """模拟raise_for_status方法"""
        if self.status_code != 200:
            raise Exception(f"HTTP {self.status_code}: {self.data.get('message', 'Unknown error')}")
    
    def json(self):
        """返回JSON数据"""
        return self.data
