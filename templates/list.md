# {{ title }}

{% for note in notes -%}
- [{{ note.title }}]({{ note.get_relative_path() }})
{% endfor %}