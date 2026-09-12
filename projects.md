---
layout: default
title: AI项目
category: AI项目
permalink: /projects/
---
{% assign enterprise_projects = site.projects | where: 'portfolio_group', 'enterprise' | sort: 'order' %}
{% assign research_projects = site.projects | where: 'portfolio_group', 'research' | sort: 'order' %}
{% assign personal_projects = site.projects | where: 'portfolio_group', 'personal' | sort: 'order' %}
{% assign lab_projects = site.projects | where: 'portfolio_group', 'labs' | sort: 'order' %}

<main class="portfolio-page">
  <section class="page-header portfolio-header">
    <p class="page-header-label">AI AGENT PORTFOLIO</p>
    <h1 class="page-header-title">AI 项目</h1>
    <p class="projects-intro">这里记录从业务问题到可验收 Agent workflow 的完整实践。项目按系统边界与证据成熟度组织：企业级系统优先展示 Context、Skills、状态、产物和回归；个人工具与实验保留在各自层级。</p>
    <nav class="portfolio-jump" aria-label="项目分区">
      <a href="#enterprise">Enterprise Agent Systems</a>
      <a href="#research">Research &amp; Data Agents</a>
      <a href="#personal">Personal AI Systems</a>
      <a href="#labs">Labs &amp; Experiments</a>
    </nav>
  </section>

  <div class="portfolio-content page-content">
    <section class="portfolio-group portfolio-group-enterprise" id="enterprise" aria-labelledby="enterprise-title">
      <div class="portfolio-group-heading">
        <div><p class="section-kicker">01 · ENTERPRISE AGENT SYSTEMS</p><h2 id="enterprise-title">企业级 Agent 系统</h2></div>
        <p>把多源资料、业务状态和长任务交付放进同一条可追溯链路。</p>
      </div>
      <div class="portfolio-card-grid portfolio-card-grid-enterprise">
        {% for project in enterprise_projects %}
        <article class="portfolio-card portfolio-card-enterprise{% if forloop.first %} portfolio-card-featured{% endif %}">
          <div class="portfolio-card-top"><span class="status-pill status-pill-{{ project.status }}">{{ project.status_label }}</span><span class="portfolio-card-order">0{{ forloop.index }}</span></div>
          <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
          <p class="portfolio-card-subtitle">{{ project.subtitle }}</p>
          <div class="portfolio-card-detail"><span>Problem</span><p>{{ project.problem }}</p></div>
          <div class="portfolio-card-detail"><span>Inputs</span><p>{{ project.inputs }}</p></div>
          <div class="portfolio-card-detail"><span>Engineering idea</span><p>{{ project.engineering }}</p></div>
          <div class="portfolio-card-bottom"><span>{{ project.evidence_label }}</span><a href="{{ project.url | relative_url }}">阅读 Case Study ↗</a></div>
        </article>
        {% endfor %}
      </div>
    </section>

    <section class="portfolio-group" id="research" aria-labelledby="research-title">
      <div class="portfolio-group-heading"><div><p class="section-kicker">02 · RESEARCH &amp; DATA AGENTS</p><h2 id="research-title">研究与数据 Agent</h2></div><p>把来源、参数、实验运行和结论放在同一条数据血缘里。</p></div>
      <div class="portfolio-card-grid">
        {% for project in research_projects %}
        <article class="portfolio-card">
          <div class="portfolio-card-top"><span class="status-pill status-pill-{{ project.status }}">{{ project.status_label }}</span><span class="portfolio-card-order">R{{ forloop.index }}</span></div>
          <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
          <p class="portfolio-card-subtitle">{{ project.subtitle }}</p>
          <div class="portfolio-card-detail"><span>Problem</span><p>{{ project.problem }}</p></div>
          <div class="portfolio-card-detail"><span>Engineering idea</span><p>{{ project.engineering }}</p></div>
          <div class="portfolio-card-bottom"><span>{{ project.evidence_label }}</span><a href="{{ project.url | relative_url }}">查看详情 ↗</a></div>
        </article>
        {% endfor %}
      </div>
    </section>

    <section class="portfolio-group" id="personal" aria-labelledby="personal-title">
      <div class="portfolio-group-heading"><div><p class="section-kicker">03 · PERSONAL AI SYSTEMS</p><h2 id="personal-title">个人 AI 信息系统</h2></div><p>从获取、解析到沉淀和展示，持续维护一条可复用的信息工作流。</p></div>
      <div class="portfolio-card-grid">
        {% for project in personal_projects %}
        <article class="portfolio-card">
          <div class="portfolio-card-top"><span class="status-pill status-pill-{{ project.status }}">{{ project.status_label }}</span><span class="portfolio-card-order">P{{ forloop.index }}</span></div>
          <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
          <p class="portfolio-card-subtitle">{{ project.subtitle }}</p>
          <p class="portfolio-card-summary">{{ project.summary }}</p>
          <div class="portfolio-card-bottom"><span>{{ project.evidence_label }}</span><a href="{{ project.url | relative_url }}">查看详情 ↗</a></div>
        </article>
        {% endfor %}
      </div>
    </section>

    <section class="portfolio-group portfolio-group-labs" id="labs" aria-labelledby="labs-title">
      <div class="portfolio-group-heading"><div><p class="section-kicker">04 · LABS &amp; EXPERIMENTS</p><h2 id="labs-title">Labs &amp; Experiments</h2></div><p>小而真实的探针，记录工具边界、失败模式和下一步判断。</p></div>
      <div class="portfolio-card-grid portfolio-card-grid-labs">
        {% for project in lab_projects %}
        <article class="portfolio-card portfolio-card-lab">
          <div class="portfolio-card-top"><span class="status-pill status-pill-{{ project.status }}">{{ project.status_label }}</span><span class="portfolio-card-order">L{{ forloop.index }}</span></div>
          <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
          <p class="portfolio-card-subtitle">{{ project.subtitle }}</p>
          <p class="portfolio-card-summary">{{ project.summary }}</p>
          <div class="portfolio-card-bottom"><span>{{ project.evidence_label }}</span><a href="{{ project.url | relative_url }}">查看详情 ↗</a></div>
        </article>
        {% endfor %}
      </div>
    </section>
  </div>
</main>
