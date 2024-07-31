{% macro generate_schema_name(custom_schema_name, node) -%}
  {% if custom_schema_name == 'refined' %}
    {{ return('refined') }}
  {% else %}
    {{ generate_schema_name_for_env(custom_schema_name, node) }}
  {% endif %}
{%- endmacro %}