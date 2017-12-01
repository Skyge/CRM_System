from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import  table_filter, table_sort
from django.shortcuts import render
from . import king_admin


def index(request):

    return render(request, "king_admin/table_index.html", {"table_list": king_admin.enabled_admins})


def display_table_objs(request, app_name, table_name):

    admin_class = king_admin.enabled_admins[app_name][table_name]
    object_list, filter_according = table_filter(request, admin_class)
    object_list, orderby_key = table_sort(request, admin_class, object_list)
    print(orderby_key)
    paginator = Paginator(object_list, admin_class.list_per_page)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)

    return render(request, "king_admin/table_objs.html", {"admin_class": admin_class,
                                                          "query_sets": query_sets,
                                                          "filter_according": filter_according,
                                                          "orderby_key":orderby_key,
                                                          "previous_orderby":request.GET.get("o", "")
                                                          })
