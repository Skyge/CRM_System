from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_app_name(admin_class):

    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):

    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(obj, admin_class):
    row_ele = ""
    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if  field_obj.choices:      # choice type
            column_data = getattr(obj, "get_{}_display".format(column))()
        else:
            column_data = getattr(obj, column)       # 通过字符串获取方法实例
        row_ele += "<td>{}</td>".format(column_data)
    return mark_safe(row_ele)
