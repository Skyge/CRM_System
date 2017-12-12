from crm import models
from django.shortcuts import render, redirect

enabled_admins = {}


class BaseAdmin():
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []
    actions = ["delete_selected_objs", ]

    def delete_selected_objs(self, request, querysets):
        print("--->delete_selected_objs", self, request, querysets)
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        if request.POST.get("delete_confirm") == "yes":
            querysets.delete()
            return redirect("/king_admin/%s/%s/" % (app_name, table_name))
        selected_ids = ','.join([str(i.id) for i in querysets])
        return render(request, "king_admin/table_obj_delete.html", {"objs": querysets,
                                                                    "admin_class": self,
                                                                    "app_name": app_name,
                                                                    "table_name": table_name,
                                                                    "selected_ids": selected_ids,
                                                                    "action": request._admin_action
                                                                    })


class CustomerAdmin(BaseAdmin):
    list_display = ["id", "qq", "name", "source", "consultant", "consult_course", "date", "status"]
    list_filters = ["source", "consultant", "consult_course", "status", "date"]
    search_fields = ["qq", "name", "consultant__name"]  # 直接关联到外键下的字段
    filter_horizontal = ("tags",)
    list_per_page = 5
    actions = ["delete_selected_objs", "test"]

    def test(self, request, querysets):
        print("Testing")
    test.display_name = "测试"


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ["customer", "consultant", "date"]


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    admin_obj = admin_class()
    admin_obj.model = model_class     # 绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_obj


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
