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
    readonly_table = False

    def delete_selected_objs(self, request, querysets):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        if self.readonly_table:
            errors = {"readonly_table": " This table is readonly, can not be modified or deleted!"}
        else:
            errors = {}
        if request.POST.get("delete_confirm") == "yes":
            if not self.readonly_table:
                querysets.delete()
            return redirect("/king_admin/%s/%s/" % (app_name, table_name))
        selected_ids = ','.join([str(i.id) for i in querysets])
        return render(request, "king_admin/table_obj_delete.html", {"objs": querysets,
                                                                    "admin_class": self,
                                                                    "app_name": app_name,
                                                                    "table_name": table_name,
                                                                    "selected_ids": selected_ids,
                                                                    "action": request._admin_action,
                                                                    "errors": errors
                                                                    })

    def default_form_validation(self):
        """允许用户可以自定义表单验证"""
        pass


class CustomerAdmin(BaseAdmin):
    list_display = ["id", "qq", "name", "source", "consultant", "consult_course", "date", "status", "enroll"]
    list_filters = ["source", "consultant", "consult_course", "status", "date"]
    search_fields = ["qq", "name", "consultant__name"]  # 直接关联到外键下的字段
    filter_horizontal = ("tags",)
    list_per_page = 5
    readonly_fields = ["qq", "consultant", "tags"]
    actions = ["delete_selected_objs", "test"]
    # readonly_table = True
    modelform_exclude_fields = []

    def test(self, request, querysets):
        print("Testing")
    test.display_name = "测试"

    def enroll(self):
        if self.instance.status == 0:
            link_name = "报名新课程"
        else:
            link_name = "报名"
        return '''<a href="/crm/customer/{}/enrollment/">{}</a>'''.format(self.instance.id, link_name)
    enroll.display_name = "报名链接"

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


class UserProfileAdmin(BaseAdmin):
    list_display = ("email", "name")
    readonly_fields = ("password",)
    filter_horizontal = ("user_permissions", "groups")
    modelform_exclude_fields = ["last_login",]


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class     # 绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
register(models.UserProfile, UserProfileAdmin)
