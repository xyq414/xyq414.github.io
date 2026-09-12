---
layout: project
title: DeepSeek Harness Workspace
subtitle: 用 Context、Skills、Memory 与 Files 让 Agent 在工作区里持续协作
description: 让 Agent 在本地项目资料中持续工作，并按来源维护项目上下文。
status: featured
status_label: 核心 Case Study
category: enterprise
portfolio_group: enterprise
group_label: Enterprise Agent Systems
featured: true
order: 2
case_study: true
role_fit: AI 产品 · FDE · AI 应用工程
problem: 企业资料很多，但“把所有文件塞进 Prompt”既昂贵又不可解释；Agent 需要知道哪些证据可用、哪些事实仍缺失。
inputs: 工作区目录、项目卡、收资分类结果、少量高价值文件正文与用户追问。
engineering: Context 是可重建的项目快照，不是事实源；按需 Review、分层加载和 provenance 让长期上下文保持可校准。
evidence_label: Context v0.2 + 本地 Harness 浏览器验收
evidence_note: 案例采用匿名项目描述；文件名、企业身份和内部产物均已从公开内容移除。
updated: 2026-09-12
tags:
  - Context Design
  - Skills
  - Workspace
  - Source Awareness
  - Rebuildable Snapshot
visibility: sanitized
summary: 基于 DeepSeek Harness 的企业工作区 Agent：从资料目录和有限正文读取建立项目 Context，通过 Skills 复核、追问和生成产物，同时保留来源、缺项、冲突与不可读边界。
---
<h2 id="overview">Overview</h2>

这个项目探索的是“企业 Agent 的工作区形态”：用户把一个项目目录交给 Agent，Agent 不会在会话开始时把所有资料全文预热，而是在明确要求 Review 时，先看目录和结构，再选择高价值文件建立一份可重建的 Context。

Context 只负责把证据组织成可工作的项目视图。原始文件、项目卡和合法外部查询仍是事实源；`project_review`、`company_lookup`、`contract_generate` 是三个清晰的能力边界。每次 Review 都能从当前目录重新生成快照，追问则复用已建立的 Context，不把旧摘要伪装成最新事实。

## Problem / Why this exists

企业项目常见的失败不是模型不会总结，而是模型不知道“这句话来自哪份文件、属于哪个角色、是否已经确认”。把 100 多份材料压成一段长 Prompt 会丢掉文件身份、缺项和冲突，也很难解释下一步为什么被阻断。

所以我把上下文拆成几类状态：**facts**（带状态与 provenance 的事实）、**material gaps**（缺文件）、**fact gaps**（有文件但事实未闭合）、**conflicts**（来源口径不同），再用 readiness、blockers、risks 和 next actions 连接到业务动作。

## Real-world inputs

| 输入层 | 处理方式 | Agent 看到的结果 |
| --- | --- | --- |
| Workspace / Source Files | 目录索引、文件类型与原件身份 | 可检索的文件树与稳定引用 |
| 材料分类结果 | 结构级收资覆盖与缺项识别 | material readiness、coverage |
| 高价值正文 | 有预算地读取少量文件，记录 reader 与定位 | 可引用的事实候选 |
| 用户问题 | 触发 Review、追问或产物动作 | 当前任务的最小 Context |

<p class="boundary-callout"><strong>来源原则：</strong>文件名可以帮助召回，但不能单独证明事实；模型分类、旧合同或历史值也不能自动成为当前交易的权威。</p>

<h2 id="architecture">System architecture</h2>

<div class="architecture-flow architecture-flow-stack" role="img" aria-label="Source Files 经过项目证据和分层 Context 后进入 Skills、Memory 和 Workspace Agent，产出新证据与反馈">
  <div class="flow-row">
    <div class="flow-node flow-node-source"><span>Source Files</span><strong>目录 · 项目卡 · 原件</strong><small>只读身份 / hash / 时间</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node"><span>Evidence</span><strong>Project evidence</strong><small>分类、正文读取、定位</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node flow-node-output"><span>L2</span><strong>Project Context</strong><small>facts · gaps · conflicts</small></div>
  </div>
  <div class="flow-rail" aria-hidden="true"></div>
  <div class="flow-row">
    <div class="flow-node"><span>Workspace</span><strong>项目知识</strong><small>当前目录与用户目标</small></div>
    <span class="flow-plus" aria-hidden="true">+</span>
    <div class="flow-node"><span>Memory</span><strong>Session / personal</strong><small>可回放的会话事实</small></div>
    <span class="flow-plus" aria-hidden="true">+</span>
    <div class="flow-node"><span>Skills</span><strong>Review · Generate</strong><small>按需加载，不常驻全文</small></div>
    <span class="flow-arrow" aria-hidden="true">→</span>
    <div class="flow-node flow-node-output"><span>Feedback</span><strong>新产物 / 新证据</strong><small>回到下一次 Context 迭代</small></div>
  </div>
</div>

## Agent workflow

1. **选择工作区**：Workspace 记录项目目录与会话归属，Agent 获得明确的文件边界。
2. **触发 Review**：用户主动要求检查项目时，Skill 调用现有材料引擎和文件读取适配器。
3. **建立证据层**：先做结构分类，再从高信息密度文件中有限读取；未读和不可读项也写入 coverage。
4. **生成 Context v0.2**：把 facts、gaps、conflicts、readiness、blockers、risks 和 next actions 组织成快照。
5. **回答与执行**：追问复用快照；明确要求时再调用主体查询或确定性产物生成。
6. **回写可审计产物**：项目判断、semantic evidence、trace 和生成文件进入 AI 产物目录，原始资料保持不变。

## Context / Skills / Memory / Files / Tools

- **Context**：项目身份、主体、容量、地点、业务状态和材料覆盖；每个事实都带 `CONFIRMED / REPORTED / CANDIDATE / UNKNOWN` 等状态。
- **Skills**：`project-review` 负责只读复核；合同生成 Skill 只消费已冻结、可填的事实；Skill 正文按需加载。
- **Memory**：Session log 记录用户问题、工具调用和回答；后续追问可以复用已建立 Context，但不会把旧快照当作新证据。
- **Files**：Source File 是可定位的证据入口，文件引用携带相对路径和原件身份；无法读取的文件明确标记为不可读。
- **Tools**：目录索引、文件读取、材料分类、主体查询和文档渲染各自有独立适配器；每个动作都可以单独验收。

## Data / evidence model

Context v0.2 维护四个互补集合：

| 集合 | 回答的问题 | 例子 |
| --- | --- | --- |
| facts | 目前知道什么，可信度如何 | 已确认的项目规模、主体或地点 |
| material_gaps | 哪类文件还没有或未被引擎确认 | 缺少某类信用材料 |
| fact_gaps | 文件存在但业务事实还没闭合 | 角色、比例、当前性未证明 |
| conflicts | 为什么不同来源不能直接合并 | 同一字段出现不同口径 |

每个事实链接到来源文件、reader、定位、时间和 hash；Context 只做投影。这样在项目资料变化后，可以重新 Review 并比较新的 evidence，而不是继续堆叠摘要。

<h2 id="evidence">Reliability &amp; validation</h2>

匿名案例的本地证据足以支持以下公开表述：

- 收资引擎对 **107 条材料结构分类为 107/107**；覆盖为 **10/11 类确认**。这是结构级证据，不等同于 107 份正文都被读过。
- Context Review 只选择 **5 个高价值文件**做语义读取，其中 **4 个可读、1 个不可读**；没有对全部材料做全文扫描。
- Context 快照包含 **25 个事实、5 个材料缺口、5 个事实缺口、3 个冲突、3 个阻塞项和 3 个风险**，并生成 5 个下一步动作；数字来自本地 `project-context` 运行证据。
- 确定性 DOCX 产物通过独立校验：压缩包包含 **29 个成员**，只填入已确认的项目名称和容量，其余 **12 个字段保持明确留空**；未确认信息没有被模型补写。
- `project_review → company_lookup → contract_generate` 的 Hero Flow 在本地 Harness 浏览器中可见；主体查询不可用时，界面保留 honest `unavailable`，不会伪造结果。

## Sanitized case study

案例使用“某 390kW 工商业光伏项目”作为匿名项目身份。资料目录较大，但 Agent 先完成结构盘点，再读取少量高价值文件：备案材料确认装机规模，补充协议提供施工责任线索，财务文件提供风险背景；一份扫描文件没有形成可用摘录，仍被标为不可读。

因此最终回答会把“已确认的规模”“尚缺的主体与工程凭证”“无法从当前资料证明的合同字段”分开呈现。用户可以先补资料、先生成带空白的内部 Demo，或明确发起只读主体查询；每条路径都保留来源和状态。

## My role

我负责把企业资料理解问题拆成 Workspace、Context、Skill 和产物边界，设计事实状态与 provenance 结构，串联既有文件引擎和确定性 renderer，并用真实浏览器验收“看得见的工作流”是否与文件证据一致。

## Current boundaries

当前实现是单主 Agent + 模块化能力，不引入第二业务数据库、RAG / 向量库或知识图谱。它适合在资料边界清楚的工作区里做可追溯复核；主体查询没有合法 provider 时会诚实失败，合同 Demo 也会保留空白。下一步优先是更好的证据选择与用户确认，而不是无边界扩大上下文。


