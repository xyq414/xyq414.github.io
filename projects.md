---
layout: default
title: 项目
category: 项目
permalink: /projects/
---
<section class="page-header">
  <p class="page-header-label">CATEGORY</p>
  <h1 class="page-header-title">项目</h1>
</section>

<section class="page-content">
  <div class="posts-list">
    {% assign projects = site.categories['项目'] %}
    {% if projects.size > 0 %}
      {% for post in projects %}
      <article class="review-card">
        <p class="review-card-category">项目</p>
        <h3 class="review-card-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        {% if post.subtitle %}
        <p class="review-card-subtitle">{{ post.subtitle }}</p>
        {% endif %}
        <p class="review-card-excerpt">{{ post.excerpt | strip_html | truncate: 120 }}</p>
        <p class="review-card-meta">{{ post.date | date: "%Y年%-m月%-d日" }}</p>
      </article>
      {% endfor %}
    {% else %}
      <div class="empty-state">还没有项目记录。用 Markdown 写完扔进 _posts/ 文件夹，category 填"项目"就行。</div>
    {% endif %}
  </div>
</section>
