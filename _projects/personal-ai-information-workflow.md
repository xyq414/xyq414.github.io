---
layout: project
title: Personal AI Information System
subtitle: 把公众号、新闻和长文资料变成可检索、可复用的个人信息系统
status: active
status_label: 持续迭代
category: personal
portfolio_group: personal
group_label: Personal AI Systems
featured: false
order: 20
case_study: true
role_fit: AI 应用工程 · 信息产品
problem: 公开内容来源分散，长文与新闻的获取、提取、摘要和归档容易变成互不相连的脚本。
inputs: 公众号链接、真实新闻 URL、市场指标、扫描 PDF 与 MinerU 结构化产物。
engineering: 获取 / 解析 / 摘要 / 沉淀 / 展示分层；LLM 只做受约束的摘要，真实 URL 与原始文本由代码保留。
evidence_label: 三条本地工作流 + 公开 HTML Demo
evidence_note: 原始文章、PDF、缓存、配置和 API 凭据均留在本地或服务器受限目录。
updated: 2026-09-12
tags:
  - Information Workflow
  - L1 / L2 / L3
  - OCR
  - Search / Summary Separation
  - HTML Output
visibility: public-demo
summary: 将公众号摘要、personal-news-briefing 与 PDF Digest 组织成一条个人信息处理流水线，并保留各子项目的独立入口。
---
<h2 id="overview">Overview</h2>

这个项目不是把几个“摘要脚本”换一个总标题，而是把个人信息处理看成一条长期维护的 pipeline：先拿到真实来源，再提取可用文本，按结构切分，生成分层摘要，最后把结果沉淀成可检索或可浏览的 HTML / Markdown。

它包含三条互补路径：

- [personal-news-briefing](/projects/personal-news-briefing/)：真实搜索与真实 URL 获取新闻候选，LLM 只做筛选与摘要，并生成每日 HTML 简报；[公开 Demo](/projects/personal-news-briefing/demo/) 保留原入口。
- [PDF Digest Pipeline](/projects/pdf-digest-pipeline/)：扫描 PDF 经过 MinerU 解析、目录筛选、章节切分和分章摘要，再导出长文阅读版。
- 公众号文章摘要：受控提取公开文章正文，输出 L1 / L2 / L3 三层摘要；服务端执行 URL 策略、限流和 body 上限。

## Problem / Why this exists

信息输入的难点经常被低估：新闻链接可能被模型编造，扫描 PDF 需要 OCR，长文摘要需要保留章节结构，公众号页面又有不同的 HTML 噪声。若获取、理解和展示混在同一个模型调用里，出错时很难知道是来源错、解析错还是摘要错。

所以每一段 pipeline 都有自己的输入和输出契约。原始 URL 与文件身份由程序保存，模型只接收已验证的文本或候选列表；低置信度的目录与摘要可以停下来复核，不用静默覆盖上一次质量更好的结果。

## Real-world inputs

| 输入 | 处理 | 输出 |
| --- | --- | --- |
| 公众号链接 / 新闻 URL | URL 规则、页面提取、标题与发布时间核验 | 真实来源与正文片段 |
| 扫描 PDF | MinerU 全书解析、噪声清理、目录页筛选 | digest-ready Markdown |
| 章节 / 新闻候选 | 分层摘要与结构化字段 | L1 / L2 / L3 或章节摘要 |
| 历史结果 | 质量判断、归档和云端 / 客户端同步 | 可浏览 HTML、Markdown、JSON |

<p class="boundary-callout"><strong>隐私边界：</strong>公开页面只展示合成或公开 Demo 输出；原始 PDF、私人文章清单、缓存、配置和密钥不随站点发布。</p>

<h2 id="architecture">System architecture</h2>

<div class="architecture-flow architecture-flow-personal" role="img" aria-label="原始链接或 PDF 经过获取、文本提取、结构切分和分层摘要，最后沉淀为 HTML、Markdown 和客户端输出">
  <div class="flow-row">
    <div class="flow-node flow-node-source"><span>Acquire</span><strong>链接 · PDF · 市场数据</strong><small>真实来源 / 原件身份</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Extract</span><strong>正文 / OCR / MinerU</strong><small>清洗噪声，保留结构</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Segment</span><strong>候选 · 章节 · 页面</strong><small>低置信度可人工确认</small></div>
  </div>
  <div class="flow-rail" aria-hidden="true"></div>
  <div class="flow-row">
    <div class="flow-node"><span>Summarize</span><strong>LLM + L1 / L2 / L3</strong><small>摘要不生成 URL</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Persist</span><strong>Markdown · JSON · archive</strong><small>可 diff、可恢复</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node flow-node-output"><span>Present</span><strong>HTML · Web · Client</strong><small>日常阅读与检索</small></div>
  </div>
</div>

## Agent workflow

### 公众号与新闻

1. 接收一条公开 URL，先执行 scheme、host、DNS / 重定向和请求大小检查。
2. 代码提取真实标题、正文片段、来源和发布时间；模型不负责生成链接。
3. LLM 从候选列表里选择重要内容并输出 L1 / L2 / L3；程序把候选索引映射回原始 URL。
4. 质量不足时保留旧结果或返回明确失败，避免低质量刷新覆盖高质量内容。

### PDF Digest

1. 对整本扫描 PDF 做 MinerU 解析，得到 `content_list`、Markdown、图片和中间结构。
2. 清理页眉页脚等噪声，筛选目录页；低置信度目录需要人工确认。
3. 将目录标题与正文匹配后切分章节，按章节运行摘要并支持 resume。
4. 以 `final_summary.md` 作为可 diff 的源文件，再导出无图或带图 HTML 阅读版。

## Context / Skills / Memory / Files / Tools

- **Context**：一次摘要只携带经过验证的正文、候选元数据和当前任务要求，不把整个网页或整本书无边界塞进模型。
- **Skills**：网页正文提取、新闻筛选、章节切分、分层摘要和 HTML 渲染分别维护自己的契约。
- **Memory**：历史简报、章节摘要和队列状态形成可回看的个人知识轨迹；新结果按日期与来源归档。
- **Files**：URL、PDF、Markdown、JSON 和 HTML 各自有明确的 source / derived 关系；输入原件不被覆盖。
- **Tools**：解析器、OCR / MinerU、摘要客户端、渲染器和本地服务可以独立替换与测试。

## Data / evidence model

系统把“原始内容”“结构化中间层”“模型摘要”和“展示投影”分开保存：

```text
source URL / PDF
  → extracted text / content_list
  → chapters / candidate records
  → L1 / L2 / L3 or chapter summaries
  → Markdown / JSON
  → HTML / client / web output
```

来源字段始终回到真实 URL 或原件身份。摘要可以帮助阅读，但不能取代原文，也不能把模型推断写成发布日期、作者或市场事实。

<h2 id="evidence">Reliability &amp; validation</h2>

- personal-news-briefing 的架构文档明确采用“搜索拿真实 URL、AI 只筛选摘要”的分离设计；公开 Demo 可直接查看 HTML 输出。
- PDF Digest 的 workflow 和 harness 明确要求 MinerU 结构、目录复核、章节边界、resume 与 HTML 导出，原始 PDF 和本地输出不进入 Git。
- 公众号摘要服务有 URL / SSRF 策略、重定向约束、正文提取、摘要格式、body 限制和限流测试；失败时只返回普通中文提示与请求标识。
- 三条路径都支持从中间产物恢复：Markdown / JSON 是可 diff 的记录，HTML 是可替换的阅读投影。

## My role

我负责把“抓取—理解—展示”拆成可观察的阶段，设计 L1 / L2 / L3 输出、来源字段和失败恢复，维护公开 Demo 与本地工作流之间的边界。重点是让每天的信息处理可重复，而不是追求一次性生成最长的摘要。

## Current boundaries

这是个人信息系统，不是通用搜索引擎，也不保证所有站点都可抓取。摘要质量受来源页面、OCR 结果和模型响应影响；系统会保留限制并允许人工复核。所有真实配置、私人数据和服务凭据都留在受限运行环境。

