#!/bin/sh

# 检查文件是否存在，如果不存在则创建
if [ ! -f /app/.output/public/config.js ]; then
  echo "window.__KB_API_VAR__ = '__KB_API__';" > /app/.output/public/config.js
  echo "window.__AI_API_VAR__ = '__AI_API__';" >> /app/.output/public/config.js
fi

# 更安全的替换方式，先检查文件是否存在
if [ -f /app/.output/public/config.js ]; then
  sed -i "s~__KB_API__~$KB_API~g" /app/.output/public/config.js
  sed -i "s~__AI_API__~$AI_API~g" /app/.output/public/config.js
fi

# 对于其他文件，使用更兼容的通配符处理方式
find /app/.output/public/_nuxt -name "*.js" -type f -exec sed -i "s~__KB_API__~$KB_API~g" {} \; 2>/dev/null || true
find /app/.output/public/_nuxt -name "*.js" -type f -exec sed -i "s~__AI_API__~$AI_API~g" {} \; 2>/dev/null || true

find /app/.output/server/chunks/build -name "*.mjs" -type f -exec sed -i "s~__KB_API__~$KB_API~g" {} \; 2>/dev/null || true
find /app/.output/server/chunks/build -name "*.mjs" -type f -exec sed -i "s~__AI_API__~$AI_API~g" {} \; 2>/dev/null || true

echo "KB_API=$KB_API" 
echo "AI_API=$AI_API" 

node -v

# 检查入口文件是否存在
if [ -f /app/.output/server/index.mjs ]; then
  node /app/.output/server/index.mjs
else
  echo "Error: /app/.output/server/index.mjs not found"
  ls -la /app/.output/server/ 2>/dev/null || echo "Server directory does not exist"
  exit 1
fi