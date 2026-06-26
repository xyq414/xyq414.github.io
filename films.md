---
layout: default
title: 电影
permalink: /films/
---
<section class="page-header">
  <p class="page-header-label">看过 · 收藏</p>
  <h1 class="page-header-title">电影</h1>
</section>

<section class="page-content">
  {% assign all_films = site.data.films %}
  {% assign total = all_films | size %}
  {% assign per_page = 30 %}
  {% assign total_pages = total | minus: 1 | divided_by: per_page | plus: 1 %}

  <div class="book-list-header">
    <p class="book-list-stats">共 <span>{{ total }}</span> 部看过</p>
    <div class="book-search">
      <input type="text" id="filmSearch" placeholder="搜索电影名或 IMDb…" autocomplete="off">
    </div>
  </div>

  <div class="book-list" id="filmList">
    {% for film in all_films %}
    <div class="book-item" data-title="{{ film.title | escape }}" data-imdb="{{ film.imdb | default: '' }}">
      <span class="book-index">{{ forloop.index }}</span>
      <div class="book-info">
        <p class="book-date">{{ film.date }}</p>
        <h3 class="book-title">
          <a href="{{ film.url }}" target="_blank" rel="noopener">《{{ film.title }}》</a>
        </h3>
        {% if film.comment %}
        <p class="book-comment">{{ film.comment | newline_to_br }}{% if film.rating %} <span class="book-rating">（{{ film.rating }}/10）</span>{% endif %}</p>
        {% elsif film.rating %}
        <p class="book-comment"><span class="book-rating">（{{ film.rating }}/10）</span></p>
        {% endif %}
      </div>
      {% if film.imdb %}
      <span class="film-imdb"><a href="https://www.imdb.com/title/{{ film.imdb }}/" target="_blank" rel="noopener">{{ film.imdb }}</a></span>
      {% endif %}
    </div>
    {% endfor %}
  </div>

  <!-- Pagination -->
  <div class="book-pagination" id="filmPagination">
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
</section>

<script>
(function() {
  var PER_PAGE = 30;
  var input = document.getElementById('filmSearch');
  var items = document.querySelectorAll('#filmList .book-item');
  var pagination = document.getElementById('filmPagination');
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
      var imdb = item.getAttribute('data-imdb') || '';
      if (!q || title.indexOf(q) !== -1 || imdb.indexOf(q) !== -1) {
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
