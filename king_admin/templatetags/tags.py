from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta

register = template.Library()


@register.simple_tag
def render_app_name(admin_class):

    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):

    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(request, obj, admin_class):
    row_ele = ""
    for index, column in enumerate(admin_class.list_display):
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:      # choice type
            column_data = getattr(obj, "get_{}_display".format(column))()
        else:
            column_data = getattr(obj, column)       # 通过字符串获取方法实例
        if type(column_data).__name__ == "datetime":
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if index == 0:
            column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                        obj_id=obj.id,
                                                                                        data = column_data)
        row_ele += "<td>{}</td>".format(column_data)
    return mark_safe(row_ele)


@register.simple_tag
def build_paginator(query_sets, filter_according, previous_orderby,  search_text):
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
            page_btns += '''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>'''  \
                         % (ele_class, page_num, filters, previous_orderby, search_text, page_num)
        # elif abs(query_sets.number - page_num) <= 1:
        #     ele_class = ""
        #     if query_sets.number == page_num:
        #         added_dot_ele = False
        #         ele_class = "active"
        #     page_btns += '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (ele_class, page_num, filters, page_num)
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
def render_filter_ele(filter_field, admin_class, filter_according):
    select_ele = '''<select class="form-control" name="{filter_field}" ><option value=''>----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)
    if field_obj.choices:
        selected = ""
        for choice_item in field_obj.choices:
            if filter_according.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ""

    if type(field_obj).__name__ == "ForeignKey":
        selected = ""
        for choice_item in field_obj.get_choices()[1:]:
            if filter_according.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ""

    if type(field_obj).__name__ in ["DateTimeField", "DateField"]:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(["今天", today_ele])
        date_els.append(["昨天", today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["本年", today_ele.replace(month=1, day=1)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])
        selected = ""
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])
        filter_field_name = "{}__gte".format(filter_field)
    else:
        filter_field_name = filter_field
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)
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


@register.simple_tag
def get_model_name(admin_class):

    return admin_class.model._meta.verbose_name
