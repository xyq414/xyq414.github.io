# AGENTS.md - personal-site

## 项目目标
维护和更新个人博客网站，包括书评、影评、乐评、随笔等内容。

## 当前状态
usable - 可用，GitHub Pages 在线。

## 运行方式
bundle exec jekyll serve（本地）
或推送到 GitHub Pages 仓库自动部署。

## 技术栈
Jekyll, HTML/CSS, Python (豆瓣数据抓取)

## Agent 工作规则
- 新博文放入 _posts/，文件名格式 YYYY-MM-DD-标题.md。
- front matter 必须包含 layout, title, category, date。
- Python 脚本用于批量抓取和格式化豆瓣数据。
- 不要硬编码豆瓣 Cookie，使用环境变量或配置文件。

## 安全注意事项
- fix_content_v2.py 中的豆瓣 Cookie 已脱敏为占位符。
- 不要上传个人隐私数据。
- _data/ 中的 JSON 是个人读书/观影记录。

## 下一步任务
- 补充 projects 页面内容。
- 考虑迁移到新仓库后如何部署。

## 特殊偏好
- 博文用中文撰写。
- 书评/影评/乐评使用 douban_url 字段关联豆瓣。