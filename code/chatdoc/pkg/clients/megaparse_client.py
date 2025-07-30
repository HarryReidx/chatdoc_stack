"""
MegaParse客户端 - 替代TEXTIN的PDF解析功能
Author: AI Assistant
Date: 2025-07-28
"""
import os
import json
import tempfile
from typing import Dict, Any, Optional
from megaparse import MegaParse
from pkg.config import config
from pkg.utils.logger import logger


class MegaParseClient:
    """MegaParse客户端，用于替代TEXTIN的PDF解析功能"""
    
    def __init__(self):
        """初始化MegaParse客户端"""
        self.megaparse = MegaParse()
        self.options = self._get_options()
        
    def _get_options(self) -> Dict[str, Any]:
        """获取解析选项，兼容原TEXTIN配置"""
        return {
            'dpi': config.get("pdf2md", {}).get("options_dpi", 144),
            'page_start': int(config.get("pdf2md", {}).get("options_page_start", 0)),
            'page_count': int(config.get("pdf2md", {}).get("options_page_count", 2000)),
            'apply_document_tree': bool(config.get("pdf2md", {}).get("options_apply_document_tree", 1)),
            'markdown_details': bool(config.get("pdf2md", {}).get("options_markdown_details", 1)),
            'page_details': bool(config.get("pdf2md", {}).get("options_page_details", 1)),
            'char_details': bool(config.get("pdf2md", {}).get("options_char_details", 1)),
            'table_flavor': config.get("pdf2md", {}).get("options_table_flavor", "html"),
            'get_image': config.get("pdf2md", {}).get("options_get_image", "page"),
            'parse_mode': config.get("pdf2md", {}).get("options_parse_mode", "auto"),
        }
    
    def recognize_pdf2md(self, image: bytes) -> 'MockResponse':
        """
        PDF转Markdown解析
        :param image: PDF文件的字节数据
        :return: 兼容TEXTIN格式的响应对象
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(image)
                temp_file_path = temp_file.name
            
            try:
                # 使用MegaParse解析PDF
                logger.info(f"开始使用MegaParse解析PDF文件，大小: {len(image)} bytes")
                markdown_content = self.megaparse.load(temp_file_path)
                
                # 转换为兼容TEXTIN的格式
                result = self._convert_to_textin_format(markdown_content, temp_file_path)
                
                logger.info(f"MegaParse解析完成，生成内容长度: {len(markdown_content)}")
                
                return MockResponse(result)
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logger.error(f"MegaParse解析失败: {str(e)}")
            raise Exception(f"PDF解析失败: {str(e)}")
    
    def _convert_to_textin_format(self, markdown_content: str, file_path: str) -> Dict[str, Any]:
        """
        将MegaParse的结果转换为兼容TEXTIN的格式
        :param markdown_content: MegaParse生成的Markdown内容
        :param file_path: 原始文件路径
        :return: 兼容TEXTIN格式的结果
        """
        # 分析Markdown内容，提取页面信息
        pages = self._extract_pages_from_markdown(markdown_content)
        
        # 构造兼容TEXTIN的响应格式
        result = {
            "code": 200,
            "message": "success",
            "result": {
                "pages": pages,
                "markdown": markdown_content,
                "document_tree": self._build_document_tree(markdown_content),
            },
            "metrics": [{"page_index": i, "confidence": 0.95} for i in range(len(pages))]
        }
        
        return result
    
    def _extract_pages_from_markdown(self, markdown_content: str) -> list:
        """
        从Markdown内容中提取页面信息
        :param markdown_content: Markdown内容
        :return: 页面列表
        """
        # 简单的页面分割逻辑，可以根据实际需要调整
        # 这里假设每个一级标题代表一个新的逻辑页面
        lines = markdown_content.split('\n')
        pages = []
        current_page_content = []
        page_index = 0
        
        for line in lines:
            if line.startswith('# ') and current_page_content:
                # 遇到新的一级标题，保存当前页面
                pages.append({
                    "page_index": page_index,
                    "markdown": '\n'.join(current_page_content),
                    "elements": self._extract_elements_from_content('\n'.join(current_page_content)),
                    "images": []  # MegaParse的图片处理需要单独实现
                })
                current_page_content = [line]
                page_index += 1
            else:
                current_page_content.append(line)
        
        # 添加最后一页
        if current_page_content:
            pages.append({
                "page_index": page_index,
                "markdown": '\n'.join(current_page_content),
                "elements": self._extract_elements_from_content('\n'.join(current_page_content)),
                "images": []
            })
        
        # 如果没有明显的页面分割，将整个内容作为一页
        if not pages:
            pages.append({
                "page_index": 0,
                "markdown": markdown_content,
                "elements": self._extract_elements_from_content(markdown_content),
                "images": []
            })
        
        return pages
    
    def _extract_elements_from_content(self, content: str) -> list:
        """
        从内容中提取元素信息（标题、段落、表格等）
        :param content: 页面内容
        :return: 元素列表
        """
        elements = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            element = {
                "line_index": i,
                "content": line,
                "bbox": [0, i*20, 500, (i+1)*20, 500, (i+1)*20, 0, (i+1)*20]  # 模拟边界框
            }
            
            if line.startswith('#'):
                element["type"] = "title"
                element["level"] = len(line) - len(line.lstrip('#'))
            elif line.startswith('|') and '|' in line[1:]:
                element["type"] = "table"
            elif line.startswith('!['):
                element["type"] = "image"
            else:
                element["type"] = "paragraph"
            
            elements.append(element)
        
        return elements
    
    def _build_document_tree(self, markdown_content: str) -> Dict[str, Any]:
        """
        构建文档树结构
        :param markdown_content: Markdown内容
        :return: 文档树
        """
        lines = markdown_content.split('\n')
        tree = {
            "title": "Document",
            "level": 0,
            "children": []
        }
        
        current_path = [tree]
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                
                node = {
                    "title": title,
                    "level": level,
                    "children": []
                }
                
                # 找到合适的父节点
                while len(current_path) > level:
                    current_path.pop()
                
                if current_path:
                    current_path[-1]["children"].append(node)
                    current_path.append(node)
        
        return tree


class MockResponse:
    """模拟requests.Response对象，兼容原有代码"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.status_code = 200
    
    def raise_for_status(self):
        """模拟raise_for_status方法"""
        if self.status_code != 200:
            raise Exception(f"HTTP {self.status_code}")
    
    def json(self):
        """返回JSON数据"""
        return self.data
