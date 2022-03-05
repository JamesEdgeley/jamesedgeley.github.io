---
layout: programming
title: 2020
---

## 2020

{% assign days = "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25" | split: " " %}
{%for day in days%}
{%include codesnippet.html part1=day %}
{%endfor%}
