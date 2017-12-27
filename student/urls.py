from django.conf.urls import url
from . import views


#app_name = 'student'

urlpatterns = [
    url(r'^$', views.student_my_classes, name="student_my_classes"),

]
