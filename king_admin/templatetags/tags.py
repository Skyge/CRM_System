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
        if field_obj.choices:      # choice type
            column_data = getattr(obj, "get_{}_display".format(column))()
        else:
            column_data = getattr(obj, column)       # 通过字符串获取方法实例
        if type(column_data).__name__ == "datetime":
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        row_ele += "<td>{}</td>".format(column_data)
    return mark_safe(row_ele)


@register.simple_tag
def build_paginator(query_sets, filter_according, previous_orderby):
    """返回整个分页元素"""
    page_btns = ""
    filters = ""
    for k, v in filter_according.items():
        filters += "&{}={}".format(k, v)
    added_dot_ele = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages - 2 \
                        or abs(query_sets.number - page_num) <= 1:
            ele_class = ""
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns += '''<li class="%s"><a href="?page=%s%s&o=%s">%s</a></li>'''  \
                         % (ele_class, page_num, filters, previous_orderby, page_num)
        else:
            if not added_dot_ele:
                page_btns += '''<li ><a >...</a></li>'''
                added_dot_ele = True
    return mark_safe(page_btns)


@register.simple_tag
def render_page_ele(loop_counter, query_sets, filter_according):
    filters = ""
    for k, v in filter_according.items():
        filters += "&{}={}".format(k, v)
    if loop_counter < 3 or loop_counter > query_sets.paginator.num_pages - 2:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (ele_class, loop_counter, filters, loop_counter)
        return mark_safe(ele)
    return ""


@register.simple_tag
def render_filter_ele(according, admin_class, filter_according):
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' % according
    field_obj = admin_class.model._meta.get_field(according)
    if field_obj.choices:
        selected = ""
        for choice_item in field_obj.choices:
            if filter_according.get(according) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ""

    if type(field_obj).__name__ == "ForeignKey":
        selected = ""
        for choice_item in field_obj.get_choices()[1:]:
            if filter_according.get(according) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ""
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def build_table_header_column(column, orderby_key, filter_according):
    filters = ""
    for k, v in filter_according.items():
        filters += "&{}={}".format(k, v)
    ele = '''<th> <a href = "?{filters}&o={orderby_key}" > {column}</a>{sort_icon}</th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up" aria-hidden="true"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span>'''
        if orderby_key.strip("-") == column:
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ""
    else:
        orderby_key = column
        sort_icon = ""
    ele = ele.format(filters=filters, orderby_key=orderby_key, column=column, sort_icon=sort_icon)
    return mark_safe(ele)
