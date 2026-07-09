---
layout: default
title: personal-news-briefing Demo
permalink: /projects/personal-news-briefing/demo/
---
<style>
  .briefing-demo {
    max-width: 960px;
    margin: 0 auto;
    padding: 72px 24px 88px;
    color: var(--text-body);
  }

  .briefing-demo a {
    color: #E0C36A;
    text-decoration: none;
    border-bottom: 1px solid rgba(var(--accent-gold-rgb), 0.45);
  }

  .briefing-demo a:hover {
    color: var(--text-headline);
    border-color: var(--text-headline);
  }

  .briefing-hero {
    margin-bottom: 34px;
    padding-bottom: 28px;
    border-bottom: 1px solid var(--divider);
  }

  .briefing-kicker {
    margin-bottom: 10px;
    color: var(--accent-gold);
    font-size: 12px;
    letter-spacing: 4px;
    text-transform: uppercase;
  }

  .briefing-title {
    margin-bottom: 12px;
    color: var(--text-headline);
    font-family: var(--font-heading);
    font-size: 54px;
    font-style: italic;
    line-height: 1.06;
  }

  .briefing-subtitle {
    margin-bottom: 22px;
    color: #D8CEC1;
    font-size: 20px;
    line-height: 1.7;
  }

  .briefing-note {
    max-width: 840px;
    color: #C8BDAF;
    font-size: 17px;
    line-height: 1.8;
  }

  .briefing-meta-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 2px;
    margin: 28px 0 42px;
  }

  .briefing-meta-card,
  .briefing-card,
  .briefing-panel,
  .briefing-safety {
    background: var(--bg-card);
    border: 1px solid rgba(212, 168, 50, 0.16);
    border-radius: 8px;
  }

  .briefing-meta-card {
    padding: 18px;
  }

  .briefing-meta-label {
    margin-bottom: 8px;
    color: var(--text-dark);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  .briefing-meta-value {
    color: var(--text-headline);
    font-size: 15px;
    line-height: 1.45;
  }

  .briefing-section {
    margin: 44px 0;
  }

  .briefing-section h2 {
    margin-bottom: 16px;
    color: var(--text-headline);
    font-family: var(--font-heading);
    font-size: 34px;
    line-height: 1.15;
  }

  .briefing-brief-list {
    display: grid;
    gap: 12px;
    padding: 0;
    list-style: none;
  }

  .briefing-brief-list li {
    padding: 16px 18px;
    background: var(--bg-card-alt);
    border-left: 3px solid var(--accent-gold);
    color: #D4C9BB;
    font-size: 17px;
    line-height: 1.75;
  }

  .briefing-card-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  .briefing-card {
    padding: 22px;
  }

  .briefing-card h3 {
    margin-bottom: 10px;
    color: var(--text-headline);
    font-family: var(--font-heading);
    font-size: 27px;
    font-style: italic;
    line-height: 1.18;
  }

  .briefing-card p {
    margin: 0 0 14px;
    color: #C8BDAF;
    font-size: 16px;
    line-height: 1.75;
  }

  .briefing-card .why {
    color: #D6C7A7;
  }

  .briefing-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
  }

  .briefing-tag {
    display: inline-flex;
    align-items: center;
    min-height: 26px;
    padding: 3px 10px;
    border: 1px solid rgba(var(--accent-gold-rgb), 0.32);
    border-radius: 999px;
    color: #E0C36A;
    font-size: 12px;
    letter-spacing: 1px;
  }

  .briefing-panel {
    padding: 22px 24px;
  }

  .briefing-panel ul {
    display: grid;
    gap: 10px;
    margin: 0;
    padding-left: 20px;
  }

  .briefing-panel li {
    color: #CFC4B6;
    font-size: 16px;
    line-height: 1.75;
  }

  .briefing-safety {
    padding: 22px 24px;
    background: #1F1A13;
  }

  .briefing-safety p {
    margin: 0 0 10px;
    color: #D9C99E;
    font-size: 16px;
    line-height: 1.75;
  }

  .briefing-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 34px;
  }

  .briefing-button {
    display: inline-flex;
    align-items: center;
    min-height: 42px;
    padding: 9px 16px;
    border: 1px solid rgba(var(--accent-gold-rgb), 0.42);
    background: var(--bg-card-alt);
    color: #E0C36A;
    font-size: 15px;
    letter-spacing: 1px;
  }

  @media (max-width: 768px) {
    .briefing-demo { padding: 48px 20px 64px; }
    .briefing-title { font-size: 38px; }
    .briefing-subtitle { font-size: 17px; }
    .briefing-meta-grid,
    .briefing-card-grid { grid-template-columns: 1fr; }
    .briefing-section h2 { font-size: 28px; }
  }
</style>

<main class="briefing-demo">
  <section class="briefing-hero">
    <p class="briefing-kicker">Public Demo</p>
    <h1 class="briefing-title">personal-news-briefing Demo</h1>
    <p class="briefing-subtitle">公开安全的示例日报</p>
    <p class="briefing-note">这是 personal-news-briefing 的公开展示样例，用于展示信息整理、摘要分层和 HTML 报告效果。页面内容为模拟/脱敏样例，不包含真实订阅源、真实 Cookie、API key 或私人配置。</p>
  </section>

  <section class="briefing-meta-grid" aria-label="Report metadata">
    <div class="briefing-meta-card">
      <p class="briefing-meta-label">Report Date</p>
      <p class="briefing-meta-value">2026-07-09</p>
    </div>
    <div class="briefing-meta-card">
      <p class="briefing-meta-label">Mode</p>
      <p class="briefing-meta-value">Public Demo</p>
    </div>
    <div class="briefing-meta-card">
      <p class="briefing-meta-label">Coverage</p>
      <p class="briefing-meta-value">AI / Tech / Markets / Personal Workflow</p>
    </div>
    <div class="briefing-meta-card">
      <p class="briefing-meta-label">Status</p>
      <p class="briefing-meta-value">Sample, not live</p>
    </div>
  </section>

  <section class="briefing-section">
    <h2>Executive Brief</h2>
    <ul class="briefing-brief-list">
      <li>AI 工具链更新速度加快，个人知识工作流需要更稳定的摘要、筛选和归档机制。</li>
      <li>高密度市场信息更适合被拆成趋势、风险和行动提示，而不是堆成一组原始链接。</li>
      <li>简报系统的重点不是追求一次性覆盖所有信息，而是把多源输入整理成每天可读、可复盘的 HTML 报告。</li>
      <li>公开版 demo 展示输出形态；私有版可以连接真实来源和本地配置，但这些内容不会出现在公开页面中。</li>
    </ul>
  </section>

  <section class="briefing-section">
    <h2>AI & Technology</h2>
    <div class="briefing-card-grid">
      <article class="briefing-card">
        <h3>Agent workflow tools move from experiments to daily utilities</h3>
        <p>模拟摘要：一组个人自动化工具从单次测试进入日常使用阶段，重点转向稳定性、可复用提示词和结果验收。</p>
        <p class="why"><strong>Why it matters:</strong> 当工具进入每天使用的流程，日志、回滚和输出格式比单次能力展示更重要。</p>
        <div class="briefing-tags"><span class="briefing-tag">Agent Workflow</span><span class="briefing-tag">Automation</span><span class="briefing-tag">Reliability</span></div>
      </article>
      <article class="briefing-card">
        <h3>Personal knowledge pipelines need public and private outputs</h3>
        <p>模拟摘要：同一套系统可以生成内部完整报告，也可以生成公开安全版本，用于展示结构和方法而不暴露私有来源。</p>
        <p class="why"><strong>Why it matters:</strong> public/private 分离能让项目适合求职展示，同时保护真实配置和个人信息源。</p>
        <div class="briefing-tags"><span class="briefing-tag">Knowledge System</span><span class="briefing-tag">Privacy Boundary</span></div>
      </article>
      <article class="briefing-card">
        <h3>HTML reports remain useful for review and archiving</h3>
        <p>模拟摘要：结构化 HTML 报告能保留标题、标签、摘要和行动提示，适合长期归档和跨设备浏览。</p>
        <p class="why"><strong>Why it matters:</strong> 比起只保存对话或纯文本，HTML 更容易承载分区阅读、重点标记和后续复盘。</p>
        <div class="briefing-tags"><span class="briefing-tag">HTML Report</span><span class="briefing-tag">Archive</span></div>
      </article>
    </div>
  </section>

  <section class="briefing-section">
    <h2>Markets & Business</h2>
    <div class="briefing-card-grid">
      <article class="briefing-card">
        <h3>Rate expectations shape capital allocation narratives</h3>
        <p>模拟摘要：市场讨论从单一价格波动转向融资成本、企业预算和长期投资节奏的组合判断。</p>
        <p class="why"><strong>Why it matters:</strong> 简报系统会优先提取影响决策的变量，而不是记录实时点位或短期噪音。</p>
        <div class="briefing-tags"><span class="briefing-tag">Macro</span><span class="briefing-tag">Risk Signal</span></div>
      </article>
      <article class="briefing-card">
        <h3>AI infrastructure spending becomes a recurring business theme</h3>
        <p>模拟摘要：企业资本开支、算力供给和软件效率之间的关系成为持续观察主题。</p>
        <p class="why"><strong>Why it matters:</strong> 这类主题适合被持续追踪，并在每日简报中归入长期趋势库。</p>
        <div class="briefing-tags"><span class="briefing-tag">AI Infrastructure</span><span class="briefing-tag">Business Trend</span></div>
      </article>
      <article class="briefing-card">
        <h3>Operational resilience matters more than one-off headlines</h3>
        <p>模拟摘要：企业应对供应、监管和需求变化的能力，比单条新闻更能解释中长期表现。</p>
        <p class="why"><strong>Why it matters:</strong> 系统会把重复出现的经营信号沉淀为后续复盘线索。</p>
        <div class="briefing-tags"><span class="briefing-tag">Business Quality</span><span class="briefing-tag">Follow-up</span></div>
      </article>
    </div>
  </section>

  <section class="briefing-section">
    <h2>Personal Workflow Notes</h2>
    <div class="briefing-panel">
      <ul>
        <li>自动整理高密度信息，把输入拆成新闻、财经、科技和个人工作流板块。</li>
        <li>标记值得后续深入阅读的主题，减少每天重新筛选信息的成本。</li>
        <li>输出 HTML 便于归档、复盘和跨设备查看。</li>
        <li>后续可扩展 latest 页面、archive 历史归档和公开安全摘要版本。</li>
      </ul>
    </div>
  </section>

  <section class="briefing-section">
    <h2>System Output Features</h2>
    <div class="briefing-panel">
      <ul>
        <li>Multi-source intake</li>
        <li>LLM summarization</li>
        <li>Sectioned briefing</li>
        <li>Risk and action extraction</li>
        <li>HTML report generation</li>
        <li>Public/private output separation</li>
      </ul>
    </div>
  </section>

  <section class="briefing-section">
    <h2>Safety Notice</h2>
    <div class="briefing-safety">
      <p>This public demo uses synthetic or sanitized content.</p>
      <p>The private version may use real sources and local configuration, but those are not included here.</p>
      <p>No API keys, cookies, private feeds, or local paths are published.</p>
    </div>
  </section>

  <nav class="briefing-actions" aria-label="Demo navigation">
    <a class="briefing-button" href="{{ '/projects/personal-news-briefing/' | relative_url }}">返回项目详情</a>
    <a class="briefing-button" href="{{ '/projects/' | relative_url }}">返回 Projects</a>
  </nav>
</main>
