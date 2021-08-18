# {{ title }}

{% for note in notes -%}
- [{{ note.title }}]({{ note.path }})
{% endfor %}