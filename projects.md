---
layout: default
title: Projects
category: AI项目
permalink: /projects/
---
{% assign groups = 'enterprise|research|personal|labs' | split: '|' %}
<main class="projects-directory"><header class="directory-head"><p>Selected work</p><h1>Projects</h1></header>{% for group in groups %}{% assign items = site.projects | where: 'portfolio_group', group | sort: 'order' %}<section class="directory-group" id="{{ group }}"><h2>{% if group == 'enterprise' %}Work{% elsif group == 'research' %}Research{% elsif group == 'personal' %}Personal{% else %}Labs{% endif %}</h2><ol>{% for project in items %}<li><a href="{{ project.url | relative_url }}"><span>{{ project.title }}<em>{{ project.description }}</em></span><small>{% if group == 'enterprise' %}{{ forloop.index | prepend: '0' }}{% else %}{{ project.category | default: '' }}{% endif %}</small><b>↗</b></a></li>{% endfor %}</ol></section>{% endfor %}</main>

