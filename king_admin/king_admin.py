from crm import models

enabled_admins = {}


class BaseAdmin():
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []


class CustomerAdmin(BaseAdmin):
    list_display = ["id", "qq", "name", "source", "consultant", "consult_course", "date", "status"]
    list_filters = ["source", "consultant", "consult_course", "status", "date"]
    search_fields = ["qq", "name", "consultant__name"]  # 直接关联到外键下的字段
    filter_horizontal = ("tags",)
    list_per_page = 5
    # ordering = "qq"


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
