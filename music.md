---
layout: default
title: 音乐
permalink: /music/
---
<section class="page-header">
  <p class="page-header-label">听过 · 收藏</p>
  <h1 class="page-header-title">音乐</h1>
</section>

<section class="page-content">
  {% assign all_music = site.data.music %}
  {% assign total = all_music | size %}
  {% assign per_page = 30 %}
  {% assign total_pages = total | minus: 1 | divided_by: per_page | plus: 1 %}

  <div class="book-list-header">
    <p class="book-list-stats">共 <span>{{ total }}</span> 首听过</p>
    {% if total > per_page %}
    <div class="book-search">
      <input type="text" id="musicSearch" placeholder="搜索音乐…" autocomplete="off">
    </div>
    {% endif %}
  </div>

  <div class="book-list" id="musicList">
    {% for music in all_music %}
    <div class="book-item" data-title="{{ music.title | escape }}">
      <span class="book-index">{{ forloop.index }}</span>
      <div class="book-info">
        <p class="book-date">{{ music.date }}</p>
        <h3 class="book-title">
          <a href="{{ music.url }}" target="_blank" rel="noopener">《{{ music.title }}》</a>
        </h3>
        {% if music.comment %}
        <p class="book-comment">{{ music.comment | newline_to_br }}{% if music.rating %} <span class="book-rating">（{{ music.rating }}/10）</span>{% endif %}</p>
        {% elsif music.rating %}
        <p class="book-comment"><span class="book-rating">（{{ music.rating }}/10）</span></p>
        {% endif %}
      </div>
    </div>
    {% endfor %}
  </div>

  {% if total > per_page %}
  <div class="book-pagination" id="musicPagination">
    <span class="disabled">&laquo; 上一页</span>
    {% for i in (1..total_pages) %}
      {% if i == 1 %}
      <span class="current">{{ i }}</span>
      {% else %}
      <span>{{ i }}</span>
      {% endif %}
    {% endfor %}
    <span class="disabled">下一页 &raquo;</span>
  </div>
  {% endif %}
</section>

{% if total > per_page %}
<script>
(function() {
  var PER_PAGE = 30;
  var input = document.getElementById('musicSearch');
  var items = document.querySelectorAll('#musicList .book-item');
  var pagination = document.getElementById('musicPagination');
  var currentPage = 1;
  var isSearching = false;

  function getTotalPages() {
    return Math.ceil(items.length / PER_PAGE);
  }

  function showPage(page) {
    currentPage = page;
    var start = (page - 1) * PER_PAGE;
    var end = start + PER_PAGE;
    items.forEach(function(item, i) {
      if (!isSearching) {
        item.style.display = (i >= start && i < end) ? '' : 'none';
      }
    });
    renderPagination();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function renderPagination() {
    if (isSearching) {
      pagination.style.display = 'none';
      return;
    }
    pagination.style.display = '';
    var total = getTotalPages();
    if (total <= 1) { pagination.innerHTML = ''; return; }

    var html = '';
    if (currentPage > 1) {
      html += '<a href="javascript:void(0)" data-page="' + (currentPage - 1) + '">&laquo; 上一页</a>';
    } else {
      html += '<span class="disabled">&laquo; 上一页</span>';
    }
    for (var i = 1; i <= total; i++) {
      if (i === currentPage) {
        html += '<span class="current">' + i + '</span>';
      } else {
        html += '<a href="javascript:void(0)" data-page="' + i + '">' + i + '</a>';
      }
    }
    if (currentPage < total) {
      html += '<a href="javascript:void(0)" data-page="' + (currentPage + 1) + '">下一页 &raquo;</a>';
    } else {
      html += '<span class="disabled">下一页 &raquo;</span>';
    }
    pagination.innerHTML = html;

    pagination.querySelectorAll('a[data-page]').forEach(function(link) {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        showPage(parseInt(this.getAttribute('data-page')));
      });
    });
  }

  input.addEventListener('input', function() {
    var q = this.value.trim().toLowerCase();
    isSearching = q.length > 0;

    items.forEach(function(item) {
      var title = (item.getAttribute('data-title') || '').toLowerCase();
      if (!q || title.indexOf(q) !== -1) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });

    if (isSearching) {
      pagination.style.display = 'none';
    } else {
      showPage(1);
    }
  });

  showPage(1);
})();
</script>
{% endif %}
