
def table_filter(request, admin_class):
    """进行条件过滤并返回过滤后的数据"""
    filter_conditions = {}
    for k, v in request.GET.items():
        if k == "page" or k == "o":     # 分页保留的关键字 and 排序关键字
            continue
        if v:
            filter_conditions[k] = v

    return admin_class.model.objects.filter(**filter_conditions), filter_conditions


def table_sort(request, admin_class, objs):
    orderby_key = request.GET.get("o")
    if orderby_key:
        res = objs.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key = "-{}".format(orderby_key)
    else:
        res = objs
    return res, orderby_key
