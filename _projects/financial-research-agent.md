---
layout: project
title: Financial Research Agent
subtitle: 量化策略开发与项目尽调中的证据分层工作流
status: active
status_label: 研究工作流
category: research
portfolio_group: research
group_label: Research & Data Agents
featured: false
order: 10
case_study: true
role_fit: AI 产品 · 研究工程 · FDE
problem: 研究结论容易把原始数据、项目方主张、模型计算和分析推断混成同一种“事实”，导致结果难以复算或复核。
inputs: 原始数据快照、来源元数据、预注册假设、BP / 访谈材料与公开资料。
engineering: 用 Source File、Context、Prompt 和 experiment / run 标识建立证据分层；LLM 辅助整理与解释，确定性脚本负责计算、复算和报告。
evidence_label: 研究仓库、冻结实验、报告台账与复算测试
evidence_note: 公开页面展示方法与已核实的研究链路；不展示账号、数据供应商凭据或未授权项目材料。
updated: 2026-09-12
tags:
  - Quant Research
  - Due Diligence
  - Data Lineage
  - Evidence Tiers
  - Reproducibility
visibility: sanitized
summary: 面向金融研究的 Agent workflow：从数据与材料进入，到假设、实验、复核和报告输出，明确区分证据等级与当前限制。
---
<h2 id="overview">Overview</h2>

这条工作流把金融 AI 分成两个相互关联、但不混淆的方向：一条是量化策略开发，另一条是私募 / 项目尽调的 Research Agent。共同原则是先建立证据地图，再让模型参与整理、提问和解释；计算、版本、来源和结论状态始终可以回到确定性产物。

当前公开证据以个人指数研究实验室为主：它已经具备数据目录、预注册假设、冻结实验、正式报告和复算链。尽调方向则沿用同一套 Source File / Context / Prompt 设计，重点放在证据分层与访谈问题生成，不把尚未核实的项目方说法写成结论。

## Problem / Why this exists

金融研究中的“正确”有两层：算式是否正确，以及证据是否有资格支持这个判断。一个模型可以把 BP、访谈纪要、外部新闻和测算表总结得很流畅，却无法凭语言本身证明来源独立、时间点正确或主体确实做过这件事。

因此，系统把每个事实放进明确的证据层，并记录输入快照、参数、运行 ID、结果和人工解释。失败、样本不足、数据缺口和 `inconclusive` 都是合法结果，不会为了得到一个漂亮的排名而被覆盖。

## Real-world inputs

| 来源 | 允许的作用 | 需要保留的上下文 |
| --- | --- | --- |
| 原始行情 / 指标快照 | 计算与复算 | 获取时间、字段语义、快照身份、质量报告 |
| 预注册假设与参数 | 锁定实验设计 | 阈值、窗口、样本切分、版本 |
| BP、访谈纪要、技术资料 | 形成项目方主张与问题清单 | 原文定位、说话人角色、时间 |
| 外部公开资料 / 独立研究 | 交叉核验与反证 | 发布主体、日期、独立性、链接 |

<p class="boundary-callout"><strong>证据边界：</strong>项目方主张可以进入 Context，但必须和外部事实、模型测算、分析推断分开显示；没有来源或时间点的数字不进入结论层。</p>

<h2 id="architecture">System architecture</h2>

<div class="architecture-flow architecture-flow-research" role="img" aria-label="Source Files 进入可追溯 Context，经过假设与实验运行，输出复算结果、研究报告和尽调问题">
  <div class="flow-row">
    <div class="flow-node flow-node-source"><span>Source Files</span><strong>数据 · BP · 纪要 · 公开资料</strong><small>原件 / 时间 / 来源</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Context</span><strong>证据分层</strong><small>主张 · 外部事实 · 测算 · 推断</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Prompt</span><strong>问题与假设</strong><small>预注册 / 访谈问题 / 复核任务</small></div>
  </div>
  <div class="flow-rail" aria-hidden="true"></div>
  <div class="flow-row">
    <div class="flow-node"><span>Run</span><strong>确定性计算</strong><small>参数、代码、快照、run ID</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Review</span><strong>稳健性与证据核验</strong><small>样本外 / 反证 / 限制</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node flow-node-output"><span>Output</span><strong>报告 / 问题 / 下一步</strong><small>可复算、可引用、可追问</small></div>
  </div>
</div>

## Agent workflow

### A. 量化策略开发

1. 先探测数据源并登记字段语义、覆盖范围和质量限制。
2. 在查看结果前冻结假设、阈值、窗口和样本切分，生成 experiment / run 身份。
3. AI Agent 辅助整理数据字典、实验说明和结果摘要；pandas / scipy 等确定性代码执行计算。
4. 对结果做稳健性、非重叠、样本外和失败分析，再生成 Markdown / HTML 报告。
5. 把报告、manifest、哈希和正式台账作为可重建投影；不把研究结果直接变成交易指令。

### B. 私募 / 项目尽调 Research Agent

1. 将 BP、访谈纪要、技术资料和公开资料按来源与角色分层。
2. 为每个主张建立 Source File → Context → Prompt 链，明确需要补问或交叉验证的地方。
3. Agent 生成市场、竞争、技术和商业模式问题，以及汇报材料的结构草稿。
4. 对关键数字和身份做外部核验或确定性测算；冲突保留为冲突，不用模型偏好消解。
5. 输出证据表、访谈问题、待验证清单和研究叙事，供人做最终判断。

## Context / Skills / Memory / Files / Tools

- **Context**：当前假设、输入快照、变量定义、已核验证据和待验证事项；不把全部原始文件拼成一个 Prompt。
- **Skills**：数据整理、指标构建、统计解释、报告生成、尽调问题设计是不同 Skill；它们共享来源引用格式。
- **Memory**：experiment / run / report ID 记录一次研究的参数与结论，旧结果保留，新的假设另起身份。
- **Files**：原始数据和研究材料只读保存；派生 Parquet、JSON、HTML 和台账是可重建投影。
- **Tools**：确定性计算、质量检查、复算、模板渲染和链接校验负责可验收部分；LLM 不能修改冻结数据。

## Data / evidence model

| 证据层 | 可回答的问题 | 不能越界成为什么 |
| --- | --- | --- |
| 项目方主张 | 对方如何描述产品、市场和进展 | 独立事实或已验证结果 |
| 外部公开事实 | 公开来源能确认什么 | 对未来表现的保证 |
| 模型 / 数据测算 | 在给定输入和参数下算出什么 | 因果证明或交易建议 |
| 分析推断 | 基于前述证据的解释与下一步 | 已确认的客观事实 |

每层都保留来源、时间、定位、参数和不确定性。报告正文优先回答“样本是什么、效果多大、证据是否稳定、限制在哪里”；详细统计与机器审计材料作为可追溯附录。

<h2 id="evidence">Reliability &amp; validation</h2>

研究仓库的当前状态快照记录了 **15 份正式报告、42 个数据集、5 个特征和 21 条数据血缘关系**；这些是研究台账与目录的工程规模，不是投资业绩。前瞻链明确区分历史回放与真实前瞻，未到期结果不会被写成命中率。

在最近一次冻结实验中，**180 / 180** 条 fixture 回放以 `1e-12` 容差通过；正式报告还通过独立 R1 / R2 复核与本地桌面 / 移动浏览器验收。研究链保留 `SUPPORTED`、`NOT_SUPPORTED` 和 `INCONCLUSIVE` 三类结果，失败结论同样进入知识库。

## Sanitized case study

一个匿名尽调任务可以这样运行：Agent 先读取项目方 BP 和访谈纪要，列出“收入规模、客户集中度、技术路线、竞争壁垒”等主张；随后把每条主张映射到公开资料和可复算测算，标出仍缺少的证明。汇报材料里同时出现“对方声称”“公开资料确认”“模型测算”和“分析推断”四个标签，读者可以沿着来源回看，而不是只看到一个综合分数。

## My role

我负责研究对象、证据层级、实验协议、数据血缘和报告契约，把模型的辅助价值放进可复算的流程里。对产品 / FDE 视角而言，重点不是自动给出买卖答案，而是让每个结论都能回答“输入是什么、谁算的、何时算的、哪里可能错”。

## Current boundaries

量化研究系统不自动交易、不提供个股买卖建议；部分数据源的严格 point-in-time 属性仍有明确限制。尽调 Research Agent 的公开内容是方法与工作流示例，不代表对任何项目或公司的投资判断。只有经过来源核验、参数冻结和人工复核的结果，才进入正式报告层。

