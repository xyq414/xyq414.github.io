---
layout: project
title: WeCom AI Agent
subtitle: 在真实业务入口里组合合同、融资资料、测算与问答 Skills
status: featured
status_label: 核心 Case Study
category: enterprise
portfolio_group: enterprise
group_label: Enterprise Agent Systems
featured: true
order: 3
case_study: true
role_fit: AI 产品 · FDE · AI 应用工程
problem: 业务请求从企业微信进入，往往同时包含文件、规则、长期状态和需要确认的事实；单轮聊天无法安全承接长任务。
inputs: 企业微信消息与文件、项目资料包、合同模板、业务规则和用户确认。
engineering: LLM 做理解与候选提取，确定性 Runtime 负责 Skill 路由、事实账本、状态恢复、文档渲染、校验和交付。
evidence_label: Runtime 2.0、版本化 Schema、Golden / 回归测试
evidence_note: 公开内容只展示架构与合成/脱敏证据；企业账号、客户合同和内部地址均不公开。
updated: 2026-09-12
tags:
  - WeCom
  - Skills
  - Deterministic Execution
  - Contract Workflow
  - Delivery
visibility: sanitized
summary: 企业微信作为真实业务入口，Agent 通过可组合 Skills 理解请求与资料，再由确定性工作流完成事实确认、计算、合同生成、独立校验和产物返回。
---
<h2 id="overview">Overview</h2>

企业微信 AI Agent 是一个“入口层 + 业务能力层 + 确定性执行层”的组合。用户可以在同一个对话里发起合同生成、合同审核、融资资料整理、项目测算或业务问答；Agent 先识别任务与需要的资料，再把工作交给对应 Skill。

关键设计是把“理解”与“执行”分开：LLM 可以理解自然语言、提出字段候选和解释材料，但不能直接把猜测写进合同、改写业务状态或声称附件已经发送。每个长任务都有可恢复的状态、输入快照、事实版本和逐项交付记录。

## Problem / Why this exists

文件型业务通常不是“问一句、答一句”：资料可能分批上传，字段可能冲突，合同模板有固定物理落点，生成后还要重开校验，发送失败还要重试。如果把这些步骤全部藏在 Prompt 里，用户无法知道任务卡在哪，也无法在进程重启后继续。

因此，Agent 负责把请求翻译成一个明确的 workflow；Runtime 负责节点、输入、动作和恢复；Skill 负责领域规则；原件和证据负责事实。业务规则、金额计算和文件写入均有独立的确定性边界。

## Real-world inputs

| 输入 | Skill 处理 | 交付 |
| --- | --- | --- |
| 企业微信文本 | 意图路由、任务建立、澄清问题 | 当前任务状态与下一步 |
| 单文件 / ZIP / RAR | 通用文件上下文、原件身份、解析与来源引用 | 结构化事实候选、缺项清单 |
| 合同模板与 Schema | 字段定义、物理落点、Authority 与 blank policy | DOCX / 审核结果 |
| 用户确认与修改 | 写入 User Decision 和 revision | 可审计的冻结快照 |

<p class="boundary-callout"><strong>公开边界：</strong>网站不包含 Bot ID、企业账号、真实客户名称、合同正文、手机号、内网地址、token 或 API key。</p>

<h2 id="architecture">System architecture</h2>

<div class="architecture-flow" role="img" aria-label="企业微信进入任务路由，调用 Skill 和 LLM 理解，再由确定性执行与验证生成产物并返回">
  <div class="flow-row">
    <div class="flow-node flow-node-source"><span>Entry</span><strong>企业微信</strong><small>文本 / 文件 / 任务回复</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Router</span><strong>Task / Skill</strong><small>合同 · 审核 · 资料 · 测算</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Interpret</span><strong>LLM + Context</strong><small>抽取候选 / 解释意图</small></div>
  </div>
  <div class="flow-rail" aria-hidden="true"></div>
  <div class="flow-row">
    <div class="flow-node"><span>Ledger</span><strong>Binding + Authority</strong><small>来源、角色、当前性、冲突</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Execute</span><strong>Deterministic Runtime</strong><small>计算 / 状态 / DOCX</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Validate</span><strong>Preflight + Validator</strong><small>重放事实、落点、残留</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node flow-node-output"><span>Deliver</span><strong>WeCom / H5</strong><small>文本、文件、失败可重试</small></div>
  </div>
</div>

## Agent workflow

1. **Claim**：入口为每个请求建立 task / instance，绑定用户、会话和当前资料组。
2. **Route**：根据意图选择一个 Skill；状态查询、补资料、结束或切换不会偷偷触发其他动作。
3. **Understand**：模型读取受限 Context，抽取事实候选与缺项；源文件仍是事实依据。
4. **Decide**：Binding 先证明项目和角色，Authority 再决定字段能否填入；冲突、历史值和未找到值保留具体原因。
5. **Confirm**：用户可以逐项查看来源、选择口径、修改字段或明确留空；每个决定带 revision。
6. **Freeze & execute**：冻结 schema、evidence、ledger 和 user decisions，调用确定性计算器 / DOCX writer。
7. **Validate & deliver**：独立 Preflight 重放证据与落点，交付文本和文件分别记录状态；失败项可以单独重试。

## Context / Skills / Memory / Files / Tools

- **Skills**：合同生成与审核、融资资料整理、项目测算、业务问答是可组合能力；入口只负责路由，不把所有规则塞进一个巨型 Prompt。
- **Context**：当前任务只携带必要的项目、主体、交易和文件上下文；不同任务隔离，补资料后由用户决定何时重新分析。
- **Memory**：Task / instance / attempt / revision 和事件日志保留长任务进度；进程恢复时用新的 worker identity 继续，而不是把旧结果写回当前任务。
- **Files**：原件、压缩包成员和解析视图有稳定身份与 hash；原件不覆盖，完成合同也不会成为新交易的默认输入。
- **Tools**：文件解析、字段 Authority、确定性计算、模板渲染、validator 和企业微信交付各自可替换、可测试。

## Data / evidence model

合同字段账本把“模型看到了什么”和“允许写入什么”分开：

| 状态 | 处理 |
| --- | --- |
| `CONFIRMED` / `USER_CONFIRMED` | 原件、关系和用户决定均满足要求，可以填入 |
| `DERIVED` | 所有父项都可填，由确定性规则计算 |
| `NEEDS_USER_CHOICE` / `CONFLICT` | 多口径或证据冲突，要求编号选择或留空 |
| `NOT_FOUND` / `EXTRACTION_UNCERTAIN` | 覆盖不足或读取不确定，保留原因并留空 |
| `HISTORICAL_ONLY` / `NEEDS_CURRENT_CONFIRMATION` | 只有历史值或当前交易未证明，不写入 |

每个字段还绑定项目、主体、交易角色、证据类型、原文定位、抽取版本和 policy。派生金额只能从允许填入的父项计算；模板中的法律条款保持只读。

<h2 id="evidence">Reliability &amp; validation</h2>

当前本地证据支持以下工程事实：

- Production Registry 暴露 **7 类真实参数化合同模板**；Schema 覆盖 **122 个字段出现、82 个不同字段 ID、171 个物理 targets**，并由 **21 条字段 Authority policy** 约束。
- 合同生成链包含收集资料、选项目、选合同 / 目标主体、分析、完整预览、查看来源、生成、校验和交付节点；非法输入没有副作用。
- 独立 Preflight 会重放 Evidence → Binding → Authority，核对 canonical value、用户决定、派生依赖和全部落点；未知字段可以明确留空，不用“全填”逼迫用户编造。
- 本地聚焦回归记录为 **15/15 通过**，覆盖 DOCX renderer、模板 validator、融资分类规则和弱标签保护；验证的是工程行为，不是客户业务成功率。
- 交付 manifest 将文本、Word 和审核 ZIP 分开记账；已确认成功的项不重复发送，失败项可单独重试。系统明确记录至少一次交付窗口，不声称端到端 exactly-once。

## Sanitized case study

用户在企业微信发送“根据这批资料生成一份 EPC 总包合同”，随后上传一个资料包。Agent 先建立任务并盘点材料，再显示项目、主体、价格、地址和日期等字段的来源与状态。若只有历史合同里的承包方或单价，系统会把它们标为 `HISTORICAL_ONLY`，不会自动填入当前合同。

用户可以选择正确的容量口径、确认主体，或对无法证明的字段选择“留空生成”。冻结后，确定性 renderer 只替换登记的事实落点，validator 重开 DOCX 检查模板版本、全部 targets、金额格式和旧值残留，最后把文本摘要与文件交付状态分别回传。

## My role

我负责把企业微信入口、Skill 路由、事实账本和确定性文档执行拆成可测试的边界，设计长任务恢复和交付语义，建立 Golden Case 与回归门禁，并把“模型说了什么”转换为产品上可解释的状态和用户决定。

## Current boundaries

当前合同能力只在受控 test profile 验证；正式业务 profile 的能力开放与它隔离。系统不自动签署合同、不替代法律审核、不把历史合同当作当前事实，也不公开任何企业内部身份或凭据。下一步优先是更多真实但可脱敏的 Golden Case，以及对失败交付和用户确认路径的持续回归。

