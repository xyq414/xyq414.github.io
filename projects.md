---
layout: default
title: Projects
category: 项目
permalink: /projects/
---
<section class="page-header">
  <p class="page-header-label">PROJECTS</p>
  <h1 class="page-header-title">Projects</h1>
</section>

<section class="page-content">
  <p class="book-list-stats">这里记录我用 AI agent、自动化脚本和个人工作流构建的项目。它们既是个人效率工具，也是工程实践样本，覆盖信息摘要、PDF OCR、AI 工具链、MCP / Skill 探针等方向。</p>

  {% assign sorted_projects = site.projects | sort: 'order' %}

  <h2>Featured Projects</h2>
  <div class="posts-list">
    {% for project in sorted_projects %}
      {% if project.featured %}
      <article class="review-card">
        <p class="review-card-category">{{ project.status_label }}</p>
        <h3 class="review-card-title"><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
        <p class="review-card-subtitle">{{ project.subtitle }}</p>
        <p class="review-card-excerpt">{{ project.summary }}</p>
        {% if project.tags %}
        <p class="review-card-meta">{{ project.tags | join: ' · ' }}</p>
        {% endif %}
        <p class="review-card-meta">
          <a href="{{ project.url | relative_url }}">详情</a>
          {% if project.demo_url %} · <a href="{{ project.demo_url | relative_url }}">Demo</a>{% endif %}
          {% if project.repo_url %} · <a href="{{ project.repo_url }}">GitHub</a>{% endif %}
        </p>
      </article>
      {% endif %}
    {% endfor %}
  </div>

  <h2>Labs & Experiments</h2>
  <div class="posts-list">
    {% for project in sorted_projects %}
      {% unless project.featured %}
      <article class="review-card">
        <p class="review-card-category">{{ project.status_label }}</p>
        <h3 class="review-card-title"><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
        <p class="review-card-subtitle">{{ project.subtitle }}</p>
        <p class="review-card-excerpt">{{ project.summary }}</p>
        {% if project.tags %}
        <p class="review-card-meta">{{ project.tags | join: ' · ' }}</p>
        {% endif %}
        <p class="review-card-meta"><a href="{{ project.url | relative_url }}">详情</a></p>
      </article>
      {% endunless %}
    {% endfor %}
  </div>
</section>
