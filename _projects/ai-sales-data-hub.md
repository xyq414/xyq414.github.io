---
layout: project
title: AI Sales Data Hub
subtitle: 从微信、电话、附件与 Excel，到可追溯的智能销售台账
description: 把分散的销售沟通与项目资料整理成可持续更新的销售台账。
status: featured
status_label: 核心 Case Study
category: enterprise
portfolio_group: enterprise
group_label: Enterprise Agent Systems
featured: true
order: 1
case_study: true
role_fit: AI 产品 · FDE · AI 应用工程
problem: 销售事实分散在聊天、通话、附件和表格里，无法直接支撑长期项目跟踪与下一步行动。
inputs: 微信消息、电话转写、销售笔记、附件媒体与 Excel 台账。
engineering: 先保存 raw evidence，再做抽取、实体关联和状态投影；AI 候选必须经过 provenance 与人工确认才能进入当前态。
evidence_label: 代码、schema、synthetic benchmark、UI 回归
evidence_note: 数字证据来自纯虚构 benchmark 与本地验收记录，明确不代表客户生产数据。
updated: 2026-09-12
tags:
  - Entity Resolution
  - Provenance
  - State Model
  - Cross-channel
  - Golden Case
visibility: sanitized
summary: 面向新能源 / 光伏销售团队的跨渠道事实层：保留原始证据，维护客户、联系人、项目、沟通和待办的长期关系，让后续 Agent 调用结构化业务事实。
---
<h2 id="overview">Overview</h2>

这是一个把销售资料从“散落的消息”变成“可追溯的业务状态”的系统。它服务新能源 / 光伏销售团队，入口可以是微信、电话、附件或已有台账；输出不是一段漂亮摘要，而是能继续被销售工作台、跟进 Agent 和周期性分析调用的事实投影。

我把系统拆成两条边界：原始证据永远保留，AI 只产生带来源的候选；当前状态、待办和项目变化由确定性服务维护。这样可以在同一个联系人关联多个项目、来源互相矛盾或导入重复时，保留“为什么这样判断”以及“还需要谁确认”。

## Problem / Why this exists

销售团队真正缺的不是又一个聊天窗口，而是一个能回答以下问题的长期记忆：这个人对应哪家客户、哪一个项目？最近一次沟通改变了什么？哪些结论来自原文，哪些只是模型猜测？客户说过的容量和表格里的容量不一致时，当前状态应该停在哪一步？

如果直接把全文交给模型，短期回答可能顺畅，长期却会丢失时间顺序、实体关系和证据等级。这个项目先建立稳定的业务对象，再让 Agent 在限定范围内使用它们。

## Real-world inputs

| 输入 | 进入系统后的处理 | 保留的证据 |
| --- | --- | --- |
| 微信文本、图片、文件 | 解析为 Communication / Media Asset | 原消息身份、时间、媒体引用、来源账号 |
| 电话录音与转写 | 由电话数据链路提供 Interaction / Transcript | 通话身份、转写状态、播放引用、时间 |
| 销售笔记与 Excel 台账 | 作为人工补充或既有业务对象 | 原始行、操作者、更新时间 |
| 模型抽取结果 | 只生成事实候选、关联候选和状态变化候选 | candidate、confidence、source reference、版本 |

<p class="boundary-callout"><strong>输入边界：</strong>公开展示只使用合成数据和脱敏描述。真实聊天、录音、手机号、客户文件和运行时数据库都留在私有环境。</p>

<h2 id="architecture">System architecture</h2>

<div class="architecture-flow" role="img" aria-label="微信、电话、附件和 Excel 进入证据层，再经过抽取与实体关联，形成客户项目状态和 Agent 上下文">
  <div class="flow-row">
    <div class="flow-node flow-node-source"><span>Sources</span><strong>微信 · 电话 · 附件 · Excel</strong></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>L0</span><strong>Raw evidence</strong><small>原件身份 / 时间 / hash</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>L1</span><strong>Extraction</strong><small>事实候选 / 事件归一化</small></div>
  </div>
  <div class="flow-rail" aria-hidden="true"></div>
  <div class="flow-row">
    <div class="flow-node"><span>Linking</span><strong>Customer · Contact · Project</strong><small>稳定 ID，歧义进入人工队列</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>L2 / L3</span><strong>State projection</strong><small>项目节点 · 待办 · 变化历史</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node flow-node-output"><span>Agent context</span><strong>跟进与分析</strong><small>只读调用，带 provenance</small></div>
  </div>
</div>

生产前台由共享的工作台服务读取跨渠道事实；电话、微信和台账各自保留来源所有权。导入收据、外部对象映射、Interaction / Case link、提议变化、状态变化和 follow-up plan 组成一条可重建链路，避免把“当前卡片”误当成唯一真相。

## Agent workflow

1. **Ingest**：为每次导入建立 receipt，按来源身份和外部引用去重；原始记录不被覆盖。
2. **Extract**：模型从限定的原文或转写中抽取事实、时间、行动和候选实体；无法确认的字段保持未知。
3. **Resolve**：先匹配联系人与客户，再匹配项目 / case；一个联系人对应多个相似项目时，不静默选择，转为 `NEEDS_MANUAL_SPLIT`。
4. **Propose**：生成状态变化和待办候选，带 evidence、confidence、source 和版本。
5. **Confirm**：销售确认或人工编辑后，才写入当前态；人工 revision 会保护待办不被后续同步复活。
6. **Project**：把已确认状态投影到微信、电话和台账工作区，后续 Agent 只读这些结构化事实并回指原始依据。

## Context / Skills / Memory / Tools

- **Context**：当前客户 / 项目、最近变化、开放待办和等待对方事项组成任务上下文；历史记录默认折叠，需要时再展开。
- **Memory**：长期记忆不是一段摘要，而是带时间和版本的 Case、CaseChange、ActionItem 与沟通关系。
- **Skills**：微信回复判断、跨渠道脉络、项目台账与待确认变化是不同能力面；每个面都调用同一份业务事实。
- **Files**：附件保留可携带的 source reference 和媒体状态；解析失败不会被当成“没有资料”。
- **Tools**：确定性导入、实体匹配、状态转换、查询与反馈记录由应用服务完成；模型不能直接改当前态。

## Data / evidence model

核心对象围绕 `Communication → CaseLink → SalesCase → CaseChange → CaseCurrentState → ActionItem` 组织，并为客户、联系人、项目、媒体和来源建立稳定 ID。每一条变化都记录 effective time、recorded time、actor、版本和 provenance；因此可以区分“客户原话”“模型候选”“人工确认”和“历史状态”。

公开的 synthetic 数据资产库还把输入分成 L0 raw communication、L1 business draft blocks、L2 customer time nodes、L3 project state nodes，并提供 schema catalog、manifest、expected output 和冻结 hash。它用于产品验收与回归，不被运行时当作答案捷径。

<h2 id="evidence">Reliability &amp; validation</h2>

证据来自本机代码、schema、合成 benchmark 和 UI 验收记录：

- 三个冻结 benchmark 场景（稳定推进、多项目归属歧义、停滞后恢复）覆盖 **675 条微信消息、35 次通话、34 条销售笔记**，归一化为 **744 个事件**；这些数字明确是 synthetic regression scope。
- 每个场景都保留 L1 / L2 / L3 expected outputs；重复导入、跨渠道证据、稳定 ID、可携带媒体引用和状态恢复都有固定断言。
- 多项目歧义不会被“最高置信度”吞掉；它进入人工拆分路径。停滞、覆盖和恢复会留下 supersede / lifecycle 记录。
- 正式电话台只读取 Sales Data Hub 的 Interaction / Transcript，不回退到本地旧录音路径；这让数据所有权和失败边界可审计。

## Real results / current scale

当前最可靠的规模表述是“跨渠道数据模型 + 可回归合成世界已经跑通”。生产客户数据、真实消息数和部署规模不在公开仓库中，因此这里不把 synthetic 数字写成业务成果，也不展示真实客户截图。

## Sanitized case study

在匿名的“某工商业光伏项目”里，客户同一联系人同时关联两个相似项目。聊天里出现容量更新，电话里出现交付承诺，Excel 台账仍停留在旧阶段。系统会：

1. 把三类来源存成独立 Interaction / evidence；
2. 给容量和项目归属生成候选，而不是直接改卡片；
3. 标记跨项目消息为待人工拆分；
4. 在销售确认后写入状态变化和下一步待办；
5. 让下一次 Agent 追问能够引用“哪条来源、哪个时间点、谁确认”。

## My role

我负责业务对象和状态语义、跨渠道信息架构、模型与确定性服务的边界、synthetic benchmark 设计、UI 验收和回归规则。产品决策从“摘要好不好看”转为“状态是否可解释、能否恢复、是否能被下一次工作复用”。

## Current boundaries

这是一个 local-first 的销售事实层，不自动发送客户消息、不替销售做最终归属判断，也不把 synthetic benchmark 当成真实业务表现。后续扩展会优先增加可审计的来源类型和确认流程，而不是先堆更多模型调用。


