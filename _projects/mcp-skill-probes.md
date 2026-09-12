---
layout: project
title: mcp-skill-probes
subtitle: MCP、Skill 与外部工具可用性探针
status: experimental
status_label: 实验验证
category: labs
portfolio_group: labs
group_label: Labs & Experiments
featured: false
order: 4
tags:
  - MCP
  - Codex Skills
  - Tool Probes
  - Agent Evaluation
  - Workflow Notes
demo_url:
repo_url:
visibility: mixed
updated: 2026-09-12
case_study: false
role_fit: Agent evaluation · Tooling
problem: 工具“看起来可用”不等于能进入长期工作流，需要先验证输入输出边界与失败原因。
inputs: MCP / Skill 候选、最小调用样例与失败记录。
engineering: 用小型探针记录可调用性、权限、格式和网络边界，再决定是否纳入工作流。
evidence_label: 探针脚本 + 结果记录
evidence_note: 实验记录只保留可公开的能力结论，不包含登录态、凭据或私有运行数据。
summary: 用小型探针验证 MCP、Skill 和外部工具的真实可用性，记录结果并沉淀 agent 工作流。
---
# mcp-skill-probes

## 项目定位

mcp-skill-probes 是一组面向 MCP、Skill 和外部工具的真实可用性探针。它不追求一次性大而全，而是通过小测试确认工具边界、记录结果，并把经验沉淀成可复用的 agent 工作流。

## 关注问题

- 工具是否真的可调用
- 输入输出边界是否清晰
- 失败时属于权限、网络、格式还是工具能力问题
- 哪些能力适合进入长期工作流
- 哪些能力只适合保留为实验记录

## 当前状态

实验验证中。这个项目会持续记录工具能力变化和实际使用结论。
