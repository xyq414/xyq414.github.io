---
layout: default
title: 书籍
permalink: /books/
---
<section class="page-header">
  <p class="page-header-label">已读 · 收藏</p>
  <h1 class="page-header-title">书籍</h1>
</section>

<section class="page-content">
  {% assign all_books = site.data.books %}
  {% assign total = all_books | size %}
  {% assign per_page = 30 %}
  {% assign total_pages = total | minus: 1 | divided_by: per_page | plus: 1 %}

  <div class="book-list-header">
    <p class="book-list-stats">共 <span>{{ total }}</span> 本读过</p>
    <div class="book-search">
      <input type="text" id="bookSearch" placeholder="搜索书名或 ISBN…" autocomplete="off">
    </div>
  </div>

  <div class="book-list" id="bookList">
    {% for book in all_books %}
    <div class="book-item" data-title="{{ book.title | escape }}" data-isbn="{{ book.isbn | default: '' }}">
      <span class="book-index">{{ forloop.index }}</span>
      <div class="book-info">
        <p class="book-date">{{ book.date }}</p>
        <h3 class="book-title">
          <a href="{{ book.url }}" target="_blank" rel="noopener">《{{ book.title }}》</a>
        </h3>
        {% if book.comment %}
        <p class="book-comment">{{ book.comment | newline_to_br }}{% if book.rating %} <span class="book-rating">（{{ book.rating }}/10）</span>{% endif %}</p>
        {% endif %}
      </div>
      {% if book.isbn %}
      <span class="book-isbn">{{ book.isbn }}</span>
      {% endif %}
    </div>
    {% endfor %}
  </div>

  <!-- Pagination -->
  <div class="book-pagination" id="bookPagination">
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
  var input = document.getElementById('bookSearch');
  var items = document.querySelectorAll('.book-item');
  var pagination = document.getElementById('bookPagination');
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
    // Prev
    if (currentPage > 1) {
      html += '<a href="javascript:void(0)" data-page="' + (currentPage - 1) + '">&laquo; 上一页</a>';
    } else {
      html += '<span class="disabled">&laquo; 上一页</span>';
    }
    // Page numbers
    for (var i = 1; i <= total; i++) {
      if (i === currentPage) {
        html += '<span class="current">' + i + '</span>';
      } else {
        html += '<a href="javascript:void(0)" data-page="' + i + '">' + i + '</a>';
      }
    }
    // Next
    if (currentPage < total) {
      html += '<a href="javascript:void(0)" data-page="' + (currentPage + 1) + '">下一页 &raquo;</a>';
    } else {
      html += '<span class="disabled">下一页 &raquo;</span>';
    }
    pagination.innerHTML = html;

    // Attach click handlers
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

    var visible = 0;
    items.forEach(function(item) {
      var title = (item.getAttribute('data-title') || '').toLowerCase();
      var isbn = item.getAttribute('data-isbn') || '';
      if (!q || title.indexOf(q) !== -1 || isbn.indexOf(q) !== -1) {
        item.style.display = '';
        visible++;
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

  // Initial page
  showPage(1);
})();
</script>
