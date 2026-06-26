# 个人博客网站 (personal-site)

**状态：usable**

基于 Jekyll 的个人博客网站，包含书评、影评、乐评、随笔等内容。

## 技术栈
- Jekyll (静态网站生成器)
- HTML/CSS
- Python (数据抓取脚本：豆瓣电影/图书/评论)

## 目录结构
- `_posts/` - 博文（书评、影评、随笔等）
- `_data/` - 结构化数据（books.json, films.json, essays.json, music.json）
- `_layouts/` - Jekyll 布局模板
- `assets/css/` - 样式文件
- `index.html` - 首页
- `*.md` - 内容页面（about, books, essays, films, music, projects）
- `*.py` - 数据抓取和格式化脚本

## 运行方式
```bash
bundle exec jekyll serve
```
或直接在 GitHub Pages 上部署。

## 来源
从旧仓库 xyq414.github.io 迁移 (2026-06-26)
- 豆瓣 Cookie 已脱敏。