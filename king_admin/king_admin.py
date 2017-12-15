from crm import models
from django.forms import ValidationError
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

    def default_form_validation(self):
        """允许用户可以自定义表单验证"""
        pass


class CustomerAdmin(BaseAdmin):
    list_display = ["id", "qq", "name", "source", "consultant", "consult_course", "date", "status"]
    list_filters = ["source", "consultant", "consult_course", "status", "date"]
    search_fields = ["qq", "name", "consultant__name"]  # 直接关联到外键下的字段
    filter_horizontal = ("tags",)
    list_per_page = 5
    readonly_fields = ["qq", "consultant", "tags"]
    actions = ["delete_selected_objs", "test"]

    def test(self, request, querysets):
        print("Testing")
    test.display_name = "测试"

    def default_form_validation(self):
        consult_content = self.cleaned_data.get("content", "")
        if len(consult_content) < 15:
            return ValidationError(
                    ("Field %(field)s 咨询记录内容不能少于15个字符"),
                    code = "invalid",
                    params = {"field": "content"},)

    def clean_name(self):
        if not self.cleaned_data["name"]:
            self.add_error("name", "can not be null!!!")



class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ["customer", "consultant", "date"]


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class     # 绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
