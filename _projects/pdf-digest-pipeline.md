---
layout: project
title: pdf-digest-pipeline
subtitle: 扫描 PDF OCR、章节切分与长文摘要流水线
description: 把扫描 PDF 解析、切分并整理成可阅读的章节摘要。
status: active
status_label: 持续迭代
category: personal
portfolio_group: personal
group_label: Personal AI Systems
featured: false
order: 33
case_study: false
role_fit: AI 应用工程 · 信息处理
problem: 扫描 PDF 难以检索，长文阅读需要稳定的结构与失败恢复。
inputs: 扫描 PDF、MinerU content_list / Markdown、目录页与章节正文。
engineering: 先做结构化解析与低置信度复核，再按章节摘要；Markdown 是源文件，HTML 是阅读投影。
evidence_label: 代码、workflow 文档与测试
evidence_note: 原始 PDF、OCR 产物、缓存和本地配置均留在运行目录，不作为公开素材。
tags:
  - PDF
  - OCR
  - MinerU
  - Long-form Summarization
  - Batch Workflow
demo_url:
repo_url:
visibility: private
updated: 2026-09-12
summary: 面向扫描 PDF 和长文资料的处理流水线，覆盖 OCR、目录识别、章节切分、摘要生成与 HTML 输出。
---
# pdf-digest-pipeline

## 项目定位

pdf-digest-pipeline 是一个面向扫描 PDF 和长文资料的处理流水线，用来把难以直接阅读和复用的文档转成结构化摘要与可浏览输出。

## 核心方向

- 扫描 PDF OCR
- 目录识别与章节切分
- 长文摘要与分层整理
- HTML 输出
- 批处理与失败恢复
- MinerU、本地 OCR 和 agent 工作流结合

## 当前状态

项目处于持续迭代阶段，重点是提升长文处理的稳定性、章节边界判断和失败后可恢复能力。

