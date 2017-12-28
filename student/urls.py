from django.conf.urls import url
from . import views


#app_name = 'student'

urlpatterns = [
    url(r'^$', views.student_my_classes, name="student_my_classes"),
    url(r'^studyrecords/(\d+)/$', views.study_records, name="study_records"),
    url(r'^homework_detail/(\d+)/$', views.homework_detail, name="homework_detail"),
]
