# IntFinQ-Frontend

## 项目简介

基于 vue + nuxt 开发的 [IntFinQ](https://intfinq.textin.com/) 知识库问答前端项目

实现的功能

1. 个人知识库文档上传，支持 pdf、word、图片等格式
2. 选择文件（可选择多个文件）后进行提问，查看问答记录
3. 对整个知识库进行提问
4. 问答页面：文件预览（包括缩放/旋转/文字复制/搜索等功能），多文档之间切换查看，目录展示，流式解析回答内容，答案来源溯源

以上功能，都可以在 TextIn.com 上体验使用，👉 [体验地址](https://intfinq.textin.com/)

## 项目运行

1. node 版本要求`node >= 20`
2. 依赖安装`yarn install`
3. 启动`yarn dev`

## docker 运行

`docker run -d -p 3001:3001 -e PORT=3001 -e KB_API=http://ip:3000 intfiq-frontend`

## 环境变量

| 变量   | 描述                                    |
| ------ | --------------------------------------- |
| KB_API | 后端接口地址，如：http://localhost:3000 |
