from django.conf.urls import url
from . import views


#app_name = 'student'

urlpatterns = [
    url(r'^$', views.index, name="stu_index"),

]
