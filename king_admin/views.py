from django.shortcuts import render
from . import king_admin


def index(request):

    return render(request, "king_admin/table_index.html", {"table_list": king_admin.enabled_admins})


def display_table_objs(request, app_name, table_name):

    admin_class = king_admin.enabled_admins[app_name][table_name]

    return render(request, "king_admin/table_objs.html", {"admin_class": admin_class})
