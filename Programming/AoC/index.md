---
layout: programming
title: Advent of Code
---

## List of Projects

```python
_sum=2020
_list=list(map(int,open("day01.txt").read().splitlines()))
```


```python
def firstpart(sum):
    for number in _list:
        if sum - number in _list:
         return(number * (sum - number))
print(firstpart(_sum))
```


```python
def secondpart(sum):
    for number1 in _list:
        subsum = sum - number1
        for number2 in _list:
            if subsum - number2 in _list:
                return number1 * number2 * (subsum-number2)
print(secondpart(_sum))
```


{% include blogcard.html image="sigma1.gif" author="James Edgeley" date="2020" 
location1="Advent of Code website" location1url="https://adventofcode.com/2020" 
title="AoC" subtitle="Advent of Code"
description="Solutions to the 2020 Advent of Code challenges"
url="2020" %}
