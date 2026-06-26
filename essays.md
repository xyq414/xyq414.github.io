---
layout: default
title: 杂文
category: 杂文
---

<section class="page-header">
  <p class="page-header-label">NOTES &amp; ESSAYS</p>
  <h1 class="page-header-title">杂文</h1>
</section>

<section class="page-content">
  {% assign essay_posts = site.categories['杂文'] | sort: "date" | reverse %}

  {% if essay_posts.size > 0 %}
  <div class="tag-tabs">
    <span class="tag-tab active" data-tag="思考">思考</span>
    <span class="tag-tab" data-tag="书影评">书影评</span>
  </div>

  <div class="notes-list">

    {% for post in essay_posts %}
      {% assign tag = post.tag | default: '思考' %}
      {% assign pday = post.date | date: "%d" %}
      {% assign pmonth = post.date | date: "%Y.%m" %}
      {% assign is_status = post.is_status | default: false %}

      <div class="note-item{% if is_status %} note-item-status{% endif %}" data-tag="{{ tag }}">
        <div class="note-date">
          <span class="note-date-day">{{ pday }}</span>
          <span class="note-date-month">{{ pmonth }}</span>
        </div>
        <div class="note-body">
          <h3 class="note-title">
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
          </h3>
          <p class="note-excerpt">{{ post.content | strip_html | truncate: 280 }}</p>
        </div>
      </div>
    {% endfor %}

  </div>

  <script>
  (function() {
    var tabs = document.querySelectorAll('.tag-tab');
    var items = document.querySelectorAll('.note-item');

    tabs.forEach(function(tab) {
      tab.addEventListener('click', function() {
        var tag = this.getAttribute('data-tag');

        // 切换标签高亮
        tabs.forEach(function(t) { t.classList.remove('active'); });
        this.classList.add('active');

        // 筛选文章
        items.forEach(function(item) {
          if (item.getAttribute('data-tag') === tag) {
            item.style.display = '';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });

    // 默认显示"思考"标签
    var defaultTab = document.querySelector('.tag-tab[data-tag="思考"]');
    if (defaultTab) defaultTab.click();
  })();
  </script>
  {% else %}
    <p class="empty-state">随笔散记，即将落笔…</p>
  {% endif %}
</section>
