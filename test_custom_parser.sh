#!/bin/bash

# ChatDoc 自定义解析服务测试脚本

echo "🚀 开始测试自定义文档解析服务..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker 未运行，请先启动 Docker${NC}"
    exit 1
fi

echo -e "${BLUE}📋 步骤1: 构建自定义解析服务...${NC}"
cd compose
docker-compose build custom-parser

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 自定义解析服务构建成功${NC}"
else
    echo -e "${RED}❌ 自定义解析服务构建失败${NC}"
    exit 1
fi

echo -e "${BLUE}📋 步骤2: 启动自定义解析服务...${NC}"
docker-compose up -d custom-parser

# 等待服务启动
echo -e "${YELLOW}⏳ 等待服务启动...${NC}"
sleep 10

# 检查服务健康状态
echo -e "${BLUE}📋 步骤3: 检查服务健康状态...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null; then
        echo -e "${GREEN}✅ 自定义解析服务启动成功${NC}"
        break
    else
        echo -e "${YELLOW}⏳ 等待服务启动... ($i/30)${NC}"
        sleep 2
    fi
    
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ 服务启动超时${NC}"
        echo -e "${YELLOW}📋 查看服务日志:${NC}"
        docker-compose logs custom-parser
        exit 1
    fi
done

# 测试解析服务
echo -e "${BLUE}📋 步骤4: 测试解析服务...${NC}"
echo -e "${YELLOW}📄 创建测试文件...${NC}"

# 创建一个简单的测试文本文件
cat > test_document.txt << 'EOF'
# 测试文档

这是一个测试文档，用于验证自定义解析服务。

## 章节1
这里是第一章节的内容。

### 表格示例
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |

## 章节2
这里是第二章节的内容。
EOF

# 测试解析API
echo -e "${YELLOW}🧪 测试解析API...${NC}"
response=$(curl -s -X POST "http://localhost:8080/api/v1/pdf_to_markdown" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_document.txt")

if echo "$response" | grep -q '"code": 200'; then
    echo -e "${GREEN}✅ 解析API测试成功${NC}"
    echo -e "${BLUE}📄 解析结果预览:${NC}"
    echo "$response" | python3 -m json.tool | head -20
else
    echo -e "${RED}❌ 解析API测试失败${NC}"
    echo "响应内容: $response"
fi

# 清理测试文件
rm -f test_document.txt

echo -e "${BLUE}📋 步骤5: 重启 chatdoc 服务以使用新的解析服务...${NC}"
docker-compose restart chatdoc

echo -e "${GREEN}🎉 测试完成！${NC}"
echo -e "${BLUE}📋 服务状态:${NC}"
docker-compose ps

echo -e "${YELLOW}📋 下一步操作:${NC}"
echo "1. 访问前端: http://localhost:48091"
echo "2. 上传一个PDF文件测试解析功能"
echo "3. 查看解析服务日志: docker-compose logs custom-parser"
echo "4. 查看chatdoc服务日志: docker-compose logs chatdoc"

echo -e "${BLUE}📋 如需回滚到TEXTIN API:${NC}"
echo "修改 docker-compose.yml 中的 PDF2MD_URL 为:"
echo "PDF2MD_URL=https://api.textin.com/ai/service/v1/pdf_to_markdown"
