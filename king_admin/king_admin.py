
from crm import models
from django.forms import ValidationError
from django.shortcuts import render, redirect, HttpResponse

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
    modelform_exclude_fields = []

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


class CourseRecordAdmin(BaseAdmin):
    list_display = ["from_class", "day_num", "teacher", "has_homework", "homework_title", "date"]

    def initialize_study_records(self, request, queryset):
        if len(queryset) > 1:
            return HttpResponse("只能选择一个班级")
        new_obj_list = []
        for enroll_obj in queryset[0].from_class.enrollment_set.all():
            new_obj_list.append(models.StudyRecord(
                student=enroll_obj,
                course_record=queryset[0],
                attendance=0,
                score=0
            ))
        try:
            models.StudyRecord.objects.bulk_create(new_obj_list)
        except Exception as e:
            return HttpResponse("批量初始化学习记录失败，请检查该节课是否已经有对应的学习记录！")
        return redirect("/king_admin/crm/studyrecord/?course_record={}".format(queryset[0].id))
    initialize_study_records.display_name = "初始化本节所有学员的上课记录"
    actions = ["initialize_study_records"]


class StudyRecordAdmin(BaseAdmin):
    list_display = ["student", "course_record", "attendance", "score", "date"]
    list_filters = ["course_record", "attendance", "score"]
    list_editable = ["score", "attendance"]


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class     # 绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
register(models.UserProfile, UserProfileAdmin)
register(models.CourseRecord, CourseRecordAdmin)
register(models.StudyRecord, StudyRecordAdmin)

