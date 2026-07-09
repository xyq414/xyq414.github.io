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
- 本仓库是 GitHub Pages 个人网站，线上页面是主要验收对象。除非用户明确说“只本地修改”“不要提交”“不要 push”，否则完成公开网站内容修改并通过安全检查后，应自动 commit + push 到 origin/main，方便用户直接打开线上页面验收。遇到敏感信息、force push、改 remote、大规模删除、构建明显失败、覆盖重要内容等高风险情况时，必须暂停询问用户。

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
