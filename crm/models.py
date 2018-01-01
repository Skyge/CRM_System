from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class Customer(models.Model):
    """客户表"""
    name = models.CharField(max_length=32, blank="True", null="True", help_text="用户报名后请改为真实姓名")
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank="True", null="True")
    phone = models.CharField(max_length=64, blank="True", null="True")
    id_number = models.CharField(max_length=64, blank="True", null="True")
    email = models.EmailField(verbose_name="常用邮箱", blank="True", null="True")
    source_choices = ((0, "转介绍"),
                      (1, "QQ群"),
                      (2, "官网"),
                      (3, "百度推广"),
                      (4, "知乎"),
                      (5, "市场推广")
                      )
    source = models.SmallIntegerField(choices=source_choices)
    status_choices = ((0, "已报名"),
                      (1, "未报名"),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=1)
    referral_from = models.CharField(max_length=64, blank="True", null="True", verbose_name="转介绍人QQ")
    consult_course = models.ForeignKey("Course", verbose_name="咨询课程")
    content = models.TextField(verbose_name="咨询详情")
    tags = models.ManyToManyField("Tag", blank="True", null="True")
    consultant = models.ForeignKey("UserProfile")
    memo = models.TextField(blank="True", null="True")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name = "客户表"
        verbose_name_plural = "客户表"


class Tag(models.Model):
    """客户标签"""
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户标签"
        verbose_name_plural = "客户标签"


class CustomerFollowUp(models.Model):
    """客户跟踪表"""
    customer = models.ForeignKey("Customer")
    content = models.TextField(verbose_name="跟进内容")
    follower = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)
    intention_choices = ((0, "2周内报名"),
                         (1, "1个月内报名"),
                         (2, "近期无报名计划"),
                         (3, "已在其他机构报名"),
                         (4, "已报名"),
                         (5, "已拉黑")
                         )
    intention = models.SmallIntegerField(choices=intention_choices)

    def __str__(self):
        # return"<%s : %s>" %(self.customer.qq, self.intention)
        return "<{self.customer.qq} : {self.intention}>".format(self=self)

    class Meta:
        verbose_name = "客户跟进记录"
        verbose_name_plural = "客户跟进记录"


class Course(models.Model):
    """课程信息表"""
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="周期（月）")
    outline = models.TextField(verbose_name="课程大纲")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程信息表"
        verbose_name_plural = "课程信息表"


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "校区表"
        verbose_name_plural = "校区表"


class ClassList(models.Model):
    """班级表"""
    branch = models.ForeignKey("Branch", verbose_name="校区")
    course = models.ForeignKey("Course")
    class_type_choices = ((0, "面授（脱产）"),
                          (1, "面授（周末）"),
                          (2, "网络班")
                          )
    contract = models.ForeignKey("ContractTemplate", blank=True, null=True)
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(blank="True", null="True", verbose_name="结业日期")

    def __str__(self):
        # return"%s %s %s" %(self.branch, self.course, self.semester)
        return "{self.branch} {self.course} {self.semester}".format(self=self)

    class Meta:
        unique_together = ("branch", "course", "semester")
        verbose_name = "班级表"
        verbose_name_plural = "班级表"


class CourseRecord(models.Model):
    """课程记录表"""
    from_class = models.ForeignKey("ClassList", verbose_name="班级")
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节（天）")
    teacher = models.ForeignKey("UserProfile")
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{self.from_class} {self.day_num}".format(self=self)

    class Meta:
        unique_together = ("from_class", "day_num")
        verbose_name = "上课记录"
        verbose_name_plural = "上课记录"


class StudyRecord(models.Model):
    """学习记录"""
    student = models.ForeignKey("Enrollment")
    course_record = models.ForeignKey("CourseRecord")
    attendance_choices = ((0, "已签到"),
                          (1, "迟到"),
                          (2, "缺勤"),
                          (3, "早退")
                          )
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0)
    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (0, "N/A"),
                     (-50, "D"),
                     (-100, "COPY")
                     )
    score = models.SmallIntegerField(choices=score_choices, default=0)
    memo = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{self.student} {self.course_record} {self.score}".format(self=self)

    class Meta:
        unique_together = ("student", "course_record")
        verbose_name = "学习记录表"
        verbose_name_plural = "学习记录表"


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer")
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问")
    contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意条款")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.customer} {self.enrolled_class}".format(self=self)

    class Meta:
        unique_together = ("customer", "enrolled_class")
        verbose_name = "报名表"
        verbose_name_plural = "报名表"


class Payment(models.Model):
    """缴费记录表"""
    customer = models.ForeignKey("Customer")
    course = models.ForeignKey("Course", verbose_name="所报课程")
    amount = models.PositiveIntegerField(default=500, verbose_name="数额")
    consultant = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{self.customer} {self.amount}".format(self=self)

    class Meta:
        verbose_name = "缴费记录表"
        verbose_name_plural = "缴费记录表"


# class UserProfile(models.Model):
#     """账号表"""
#     user = models.OneToOneField(User)
#     name = models.CharField(max_length=32)
#     roles = models.ManyToManyField("Role", blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "账号表"
#         verbose_name_plural = "账号表"
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """账号表"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    password = models.CharField(_('password'), max_length=128,
                                help_text=mark_safe('''<a href='password/'>修改密码</a>'''))
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    roles = models.ManyToManyField("Role", blank=True)
    objects = UserProfileManager()
    student_account = models.ForeignKey("Customer", verbose_name="关联学员账号", blank=True, null=True,
                                        help_text="只有学员报名成功后，方可为其创建账号")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        permissions = (("can_fuck_him_to_death", "可以弄死产品"),
                       ("can_access_my_course", "可以访问我的课程"),
                       ("can_access_customer_list", "可以访问客户列表"),
                       ("can_access_customer_detail", "可以访问客户详细"),
                       ("can_access_studyrecords", "可以访问学习记录页面"),
                       ("can_access_homework_detail", "可以访问作业详情页面"),
                       ("can_upload_homework", "可以交作业"),
                       ("access_kingadmin_table_obj_detail", "可以访问kingadmin每个表的对象"),
                       ("change_kingadmin_table_obj_detail", "可以修改kingadmin每个表的对象"),
                       )


class Role(models.Model):
    """权限表"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = "权限表"


class Menu(models.Model):
    """菜单"""
    name = models.CharField(max_length=32)
    url_type_choices = ((0, "related_url"), (1, "absolute_url"))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ContractTemplate(models.Model):
    """合同模板"""
    name = models.CharField("合同名称", max_length=64, unique=True)
    template = models.TextField()

    def __str__(self):
        return  self.name